"""
02_create_sample.py
Creates a stratified random sample from the full California food retail dataset.
Outputs a CSV template for manual coding with MANUAL_FORMAT and IS_ETHNIC columns.
"""

import os
import pandas as pd

# --- Configuration ---
SAMPLE_PER_STRATUM = 100  # 100 with website + 100 without = 200 total
RANDOM_SEED = 42

def main():
    # ==========================================================================
    # PATH CONFIGURATION

    # OPTION A: Command Line Execution (Default)
    # Use this when running: uv run python 02_code/02_create_sample.py
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    # project_root = os.path.dirname(script_dir)
    
    # OPTION B: Jupyter Notebook / Interactive Environment
    # Uncomment the line below and comment out OPTION A if you get:
    # "NameError: name '__file__' is not defined"
    project_root = r"C:\Users\lucaa\OneDrive\Projects\grocery-store" # Replace with your own path :)
    # ==========================================================================
    
    input_file = os.path.join(project_root, "03_output", "california_food_retail_full.parquet")
    output_dir = os.path.join(project_root, "03_output")
    output_file = os.path.join(output_dir, "california_manual_coding_sample.csv")
    
    os.makedirs(output_dir, exist_ok=True)

    # --- 2. Load Data ---
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        print("Run 01_fetch_overture.py first.")
        return
    
    print(f"Loading data from: {input_file}")
    df = pd.read_parquet(input_file)
    print(f"Total locations loaded: {len(df):,}")

    # --- 3. Stratified Sampling ---
    # Split by website presence (proxy for chain vs independent)
    df_with_web = df[df['website'].notna()]
    df_no_web = df[df['website'].isna()]
    
    print(f"\nStratification:")
    print(f"  With website: {len(df_with_web):,}")
    print(f"  Without website: {len(df_no_web):,}")
    
    sample_web = df_with_web.sample(
        n=min(SAMPLE_PER_STRATUM, len(df_with_web)), 
        random_state=RANDOM_SEED
    )
    sample_no_web = df_no_web.sample(
        n=min(SAMPLE_PER_STRATUM, len(df_no_web)), 
        random_state=RANDOM_SEED
    )
    
    # Combine and shuffle
    sample = pd.concat([sample_web, sample_no_web]).sample(
        frac=1, 
        random_state=RANDOM_SEED
    ).reset_index(drop=True)

    # --- 4. Add Coding Columns ---
    sample['MANUAL_FORMAT'] = ''  # Supermarket / Convenience / Other
    sample['IS_ETHNIC'] = ''      # 1 or 0
    sample['CONFIDENCE'] = ''     # H / M / L (optional)
    sample['NOTES'] = ''          # For edge cases
    
    # --- 5. Add Street View URL ---
    sample['streetview_url'] = sample.apply(
        lambda r: f"https://www.google.com/maps/@{r['latitude']},{r['longitude']},3a,75y,0h,90t/data=!3m4!1e1!3m2",
        axis=1
    )

    # --- 6. Reorder Columns for Coding Convenience ---
    coding_cols = ['MANUAL_FORMAT', 'IS_ETHNIC', 'CONFIDENCE', 'NOTES']
    info_cols = ['name', 'address', 'category', 'alternate_categories', 'brand_name', 'streetview_url']
    meta_cols = ['id', 'brand_id', 'website', 'phone', 'source_count', 'latitude', 'longitude']
    
    sample = sample[coding_cols + info_cols + meta_cols]

    # --- 7. Save ---
    sample.to_csv(output_file, index=False)
    
    print(f"\nSample created!")
    print(f"  Sample size: {len(sample)}")
    print(f"  Saved to: {output_file}")
    print(f"\nSample category breakdown:")
    print(sample['category'].value_counts().to_string())
    print(f"\nNext step: Open the CSV and code each row using the CODEBOOK.md")

if __name__ == "__main__":
    main()