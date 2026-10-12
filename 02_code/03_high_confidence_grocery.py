"""
03_high_confidence_grocery.py
Filters the full California food retail dataset down to HIGH-CONFIDENCE grocery stores.
Excludes convenience stores, gas stations, and ambiguous categories.

This dataset is intended for use BEFORE manual coding is complete.
It accepts Overture's classification at face value for 'supermarket' and 'grocery_store'.

Input:  03_output/california_food_retail_full.parquet (from 01_fetch_overture.py)
Output: 03_output/california_grocery_stores.{parquet,csv,dta}
"""

import os
import pandas as pd

# Include: primary category is one of these
INCLUDE_PRIMARY = ["supermarket", "grocery_store"]
# Exclude: anything also tagged with one of these in its alternate categories
EXCLUDE_ALTERNATE = {"convenience_store", "gas_station", "petrol_station", "fuel_station"}

def main():
    # ==========================================================================
    # PATH CONFIGURATION
    # ==========================================================================
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
    except NameError:
        # Interactive / Jupyter environment: assume cwd is the 02_code/ directory
        project_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
    # ==========================================================================

    output_dir = os.path.join(project_root, "03_output")
    input_file = os.path.join(output_dir, "california_food_retail_full.parquet")

    output_parquet = os.path.join(output_dir, "california_grocery_stores.parquet")
    output_csv = os.path.join(output_dir, "california_grocery_stores.csv")
    output_dta = os.path.join(output_dir, "california_grocery_stores.dta")

    # --- 1. Load Data ---
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        print("Run 01_fetch_overture.py first.")
        return

    print(f"Loading data from: {input_file}")
    df = pd.read_parquet(input_file)
    print(f"Total locations loaded: {len(df):,}")

    # --- 2. Filter: High-Confidence Grocery Only ---
    is_grocery = df['category'].isin(INCLUDE_PRIMARY)
    has_excluded_alt = df['alternate_categories'].apply(
        lambda x: x is not None and not EXCLUDE_ALTERNATE.isdisjoint(x)
    )
    df = df[is_grocery & ~has_excluded_alt].reset_index(drop=True)
    print(f"High-confidence grocery stores found: {len(df):,}")

    # --- 3. Summary Statistics ---
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    print(f"\nBy Primary Category:")
    print(df['category'].value_counts().to_string())
    print(f"\nHas Brand Name: {df['brand_name'].notna().sum():,} ({100*df['brand_name'].notna().mean():.1f}%)")
    print(f"Has Website: {df['website'].notna().sum():,} ({100*df['website'].notna().mean():.1f}%)")

    # --- 4. Save Parquet ---
    df.to_parquet(output_parquet, index=False)
    print(f"\nSaved Parquet: {output_parquet}")

    # --- 5. Save CSV ---
    df.to_csv(output_csv, index=False)
    print(f"Saved CSV: {output_csv}")

    # --- 6. Save Stata .dta ---
    df_stata = df.copy()
    df_stata['alternate_categories'] = df_stata['alternate_categories'].apply(
        lambda x: '|'.join(x) if x is not None else ''
    )
    df_stata.columns = [col[:32] for col in df_stata.columns]
    df_stata.to_stata(output_dta, write_index=False, version=118)
    print(f"Saved Stata: {output_dta}")

    print(f"\n{'='*60}")
    print(f"Total: {len(df):,} grocery stores in California")
    print('='*60)

if __name__ == "__main__":
    main()
