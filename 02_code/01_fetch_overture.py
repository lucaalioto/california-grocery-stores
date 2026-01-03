"""
01_fetch_overture.py
Downloads all potential food retail locations in California from Overture Maps.
Saves the full dataset to 03_output/ in multiple formats (Parquet, CSV, Stata).
"""

import os
import duckdb
import leafmap.leafmap as leafmap
import pandas as pd

def main():
    # --- 1. Setup ---
    MIN_LON, MIN_LAT = -124.48, 32.53
    MAX_LON, MAX_LAT = -114.13, 42.01
    
    # ==========================================================================
    # PATH CONFIGURATION (if only I could library(here))
  
    # OPTION A: Command Line Execution (Default)
    # Use this when running: uv run python 02_code/01_fetch_overture.py
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    # project_root = os.path.dirname(script_dir)
    
    # OPTION B: Jupyter Notebook / Interactive Environment
    # Uncomment the line below and comment out OPTION A if you get:
    # "NameError: name '__file__' is not defined"
    project_root = r"C:\Users\lucaa\OneDrive\Projects\grocery-store" # Replace with your own path :) 
    # ==========================================================================
    
    output_dir = os.path.join(project_root, "03_output")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Output files
    output_parquet = os.path.join(output_dir, "california_food_retail_full.parquet")
    output_csv = os.path.join(output_dir, "california_food_retail_full.csv")
    output_dta = os.path.join(output_dir, "california_food_retail_full.dta")

    # --- 2. Get Overture Release ---
    try: 
        release = leafmap.get_overture_latest_release()
    except: 
        release = "2024-11-13.0"

    # Not sure why, but the pull is giving me 2025-12-17 when online the current version is 2025-12-17.0
    release = "2025-12-17.0"
    
    url = f"s3://overturemaps-us-west-2/release/{release}/theme=places/type=place/*.parquet"
    print(f"Fetching Overture Data for California ({release})...")

    # --- 3. Connect and Configure DuckDB ---
    con = duckdb.connect(":memory:")
    con.install_extension("spatial")
    con.load_extension("spatial")
    con.install_extension("httpfs")
    con.load_extension("httpfs")
    con.sql("SET s3_region='us-west-2';")

    # --- 4. Query ---
    query = f"""
        SELECT 
            id,
            names.primary as name,
            addresses[1].freeform as address,
            
            categories.primary as category,
            list_transform(categories.alternate, x -> x) as alternate_categories,
            brand.names.primary as brand_name,
            brand.wikidata as brand_id,
            websites[1] as website,
            phones[1] as phone,
            len(sources) as source_count,
            
            ST_Y(geometry) as latitude,
            ST_X(geometry) as longitude
            
        FROM read_parquet('{url}')
        WHERE bbox.xmin >= {MIN_LON} AND bbox.xmax <= {MAX_LON} 
          AND bbox.ymin >= {MIN_LAT} AND bbox.ymax <= {MAX_LAT}
          AND (
              categories.primary IN ('grocery_store', 'supermarket', 'convenience_store', 'specialty_food_store')
              OR list_contains(categories.alternate, 'grocery_store')
              OR list_contains(categories.alternate, 'supermarket')
              OR list_contains(categories.alternate, 'convenience_store')
          )
    """
    
    print("Executing query (this may take several minutes)...")
    df = con.sql(query).df()
    
    # --- 5. Save Parquet (best for Python/pandas) ---
    df.to_parquet(output_parquet, index=False)
    print(f"Saved Parquet: {output_parquet}")
    
    # --- 6. Save CSV (universal compatibility) ---
    df.to_csv(output_csv, index=False)
    print(f"Saved CSV: {output_csv}")
    
    # --- 7. Save Stata .dta (for Stata users) ---
    # Stata has restrictions: column names <= 32 chars, no lists
    df_stata = df.copy()
    
    # Convert list column to string for Stata compatibility
    df_stata['alternate_categories'] = df_stata['alternate_categories'].apply(
        lambda x: '|'.join(x) if isinstance(x, list) else ''
    )
    
    # Truncate column names if needed (Stata 32 char limit)
    df_stata.columns = [col[:32] for col in df_stata.columns]
    
    df_stata.to_stata(output_dta, write_index=False, version=118)
    print(f"Saved Stata: {output_dta}")
    
    # --- 8. Summary ---
    print(f"\nComplete!")
    print(f"  Total locations: {len(df):,}")
    print(f"\nCategory breakdown:")
    print(df['category'].value_counts().to_string())
    print(f"\nFiles saved to {output_dir}/")

if __name__ == "__main__":
    main()