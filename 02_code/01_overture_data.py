import os
import duckdb
import leafmap.leafmap as leafmap
import osmnx as ox
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

def main():
    # --- 1. Setup ---
    MIN_LON, MIN_LAT = -121.56012, 38.437574
    MAX_LON, MAX_LAT = -121.36274, 38.685506
    bbox_tuple = (MIN_LON, MIN_LAT, MAX_LON, MAX_LAT)

    base_dir = os.getcwd()
    final_csv = os.path.join(base_dir, "sacramento_side_by_side.csv")

    # --- 2. Get OpenStreetMap (OSM) Data ---
    print(f"Fetching 'Ground Truth' from OSM...")
    tags = {'shop': ['supermarket', 'convenience', 'grocery']}
    
    try:
        gdf_osm = ox.features_from_bbox(bbox=bbox_tuple, tags=tags)
    except Exception as e:
        print(f"Error fetching OSM: {e}"); return

    # Clean OSM Data
    gdf_osm = gdf_osm.reset_index()
    gdf_osm['geometry_wkt'] = gdf_osm.geometry.apply(lambda x: x.wkt if x is not None else None)
    
    # 🔹 STEP 2A: Define EVERY column we want to compare
    cols_to_keep = [
        'name', 'shop', 
        'brand', 'brand:wikidata',       # Brand Text & ID
        'phone', 'contact:phone',        # Phones
        'website', 'contact:website',    # Websites
        'addr:housenumber', 'addr:street', 
        'opening_hours', 'geometry_wkt'
    ]
    
    clean_data = {}
    for col in cols_to_keep:
        if col in gdf_osm.columns:
            clean_data[col] = gdf_osm[col].fillna("").astype(str)
        else:
            clean_data[col] = [""] * len(gdf_osm)

    df_osm = pd.DataFrame(clean_data)
    print(f"Found {len(df_osm)} OSM locations.")

    # --- 3. Connect DuckDB ---
    con = duckdb.connect(":memory:")
    con.install_extension("spatial"); con.load_extension("spatial")
    con.install_extension("httpfs"); con.load_extension("httpfs")
    con.sql("SET s3_region='us-west-2';")
    con.register('osm_table', df_osm)

    # --- 4. Get Overture Data ---
    try:
        release = leafmap.get_overture_latest_release()
    except:
        release = "2025-12-17.0"

    # Seems to be pulling release = "2025-12-17" but I think we need "2025-12-17.0"
    release = "2025-12-17.0"
    
    overture_url = f"s3://overturemaps-us-west-2/release/{release}/theme=places/type=place/*.parquet"
    print(f"Merging with Overture Maps ({release})...")

    # --- 5. The Comparison Query ---
    query = f"""
    COPY (
        WITH osm_clean AS (
            SELECT 
                NULLIF(name, '') as name,
                NULLIF(shop, '') as osm_category,
                
                -- Normalize OSM Tags (sometimes they use different keys)
                COALESCE(NULLIF("brand:wikidata", ''), NULLIF(brand, '')) as osm_brand_id,
                NULLIF(brand, '') as osm_brand_name,
                
                COALESCE(NULLIF(phone, ''), NULLIF("contact:phone", '')) as osm_phone,
                COALESCE(NULLIF(website, ''), NULLIF("contact:website", '')) as osm_website,
                
                TRIM(CONCAT(NULLIF("addr:housenumber", ''), ' ', NULLIF("addr:street", ''))) as osm_address,
                NULLIF(opening_hours, '') as osm_opening_hours,
                ST_GeomFromText(geometry_wkt) as geom
            FROM osm_table
            WHERE NULLIF(name, '') IS NOT NULL
        ),
        overture_data AS (
            SELECT 
                id as overture_id,
                names.primary as overture_name,
                categories.primary as overture_category,
                
                -- Overture Metadata
                brand.names.primary AS overture_brand_name,
                brand.wikidata AS overture_brand_id,
                phones[1] AS overture_phone,
                websites[1] AS overture_website,
                addresses[1].freeform AS overture_address,
                
                confidence,
                geometry as geom
            FROM read_parquet('{overture_url}')
            WHERE bbox.xmin >= {MIN_LON} AND bbox.xmax <= {MAX_LON} 
              AND bbox.ymin >= {MIN_LAT} AND bbox.ymax <= {MAX_LAT}
              AND (
                  categories.primary IN ('grocery_store', 'supermarket', 'convenience_store')
                  OR list_contains(categories.alternate, 'grocery_store')
                  OR list_contains(categories.alternate, 'supermarket')
              )
        )
        SELECT 
            -- === IDENTIFIERS ===
            overture.overture_id,
            overture.overture_name,
            osm.name as osm_name,
            
            -- === TARGET LABEL (For ML) ===
            osm.osm_category as TRUE_LABEL,
            overture.overture_category,
            
            -- === BRAND COMPARISON ===
            overture.overture_brand_name,
            osm.osm_brand_name,
            
            overture.overture_brand_id,  -- Compare this...
            osm.osm_brand_id,            -- ...to this!
            
            -- === CONTACT COMPARISON ===
            overture.overture_phone,
            osm.osm_phone,
            
            overture.overture_website,
            osm.osm_website,
            
            overture.overture_address,
            osm.osm_address,
            
            -- === METADATA ===
            osm.osm_opening_hours,
            overture.confidence,
            ST_Distance(osm.geom, overture.geom) as match_dist_deg
            
        FROM osm_clean osm
        FULL OUTER JOIN overture_data overture
        ON (
            damerau_levenshtein(lower(osm.name), lower(overture.overture_name)) < 3
            OR overture.overture_name ILIKE '%' || osm.name || '%'
        )
        AND ST_DWithin(osm.geom, overture.geom, 0.001)
        
    ) TO '{final_csv}' (HEADER, DELIMITER ',');
    """
    
    con.sql(query)
    con.close()
    print(f"Side-by-Side Dataset Saved: {final_csv}")

if __name__ == "__main__":
    main()