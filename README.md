# California Grocery Stores

A research project to classify food retail environments in California using Overture Maps data. This project implements a multi-label classification system to categorize stores by Format and Ethnicity.

## Research Methodology

This project uses **Virtual Ground Truthing** via Google Street View to classify grocery stores. Researchers examine street-level imagery to determine store characteristics without requiring physical site visits.

### Classification Axes

1. **MANUAL_FORMAT** - Physical retail format and service model (e.g. `Supermarket`, `Convenience`)
2. **IS_ETHNIC** - Whether the store is oriented toward a specific cultural community (`1` = Ethnic, `0` = General)

The full list of values and the decision rules for each are in [CODEBOOK.md](CODEBOOK.md).

## Directory Structure

```
california-grocery-stores/
├── 01_data/
│   └── SNAP Retailer Location data.csv   # USDA SNAP retailers (see Data below)
├── 02_code/
│   ├── 01_fetch_overture.py              # Fetches Overture Maps data for California
│   ├── 02_create_sample.py               # Creates stratified sample for manual coding
│   └── 03_high_confidence_grocery.py     # Filters to high-confidence grocery stores
├── 03_output/                            # Generated datasets (see Data below)
├── CODEBOOK.md                           # Coding instructions for classification
├── pyproject.toml                        # Project configuration
├── uv.lock                               # Pinned package versions
└── README.md                             # This file
```

## Data

### Overture Maps (`03_output/`)

Built from the Overture Maps **places** theme.

| File | Script | Contents |
|------|--------|----------|
| `california_food_retail_full.{parquet,csv,dta}` | 01 | Every California place whose primary category is `grocery_store`, `supermarket`, `convenience_store`, or `specialty_food_store`, or whose alternate categories include `grocery_store`, `supermarket`, or `convenience_store` (43,521 locations) |
| `california_manual_coding_sample.csv` | 02 | Stratified random sample of 200 locations (100 with a website, 100 without; seed 42) with blank coding columns |
| `california_grocery_stores.{parquet,csv,dta}` | 03 | High-confidence subset: primary category `supermarket` or `grocery_store`, excluding anything also tagged `convenience_store`, `gas_station`, `petrol_station`, or `fuel_station`. Intended for use before manual coding is complete. Not included; run script 03 to create it (no download needed) |

> **Release note:** The included files were built from Overture release **`2025-12-17.0`**. Overture only keeps its most recent releases online and deletes older ones, and that release is no longer available, so `01_fetch_overture.py` is now pinned to **`2026-09-23.1`**. Re-running script 01 (and then 02) will produce slightly different data and a different random sample. If the pinned release has also been removed, update `release` in `01_fetch_overture.py` to a current one ([release list](https://docs.overturemaps.org/release/latest/)).

### SNAP retailers (`01_data/`)

`SNAP Retailer Location data.csv` is an export from the [USDA FNS SNAP Retailer Locator](https://usda-fns.maps.arcgis.com/apps/webappviewer/index.html?id=15e1c457b56c4a729861d015cd626a23) (pulled April 2026). It covers the Sacramento region (Sacramento, Yolo, Placer, and Solano counties; 419 retailers) and was pre-filtered on the website to four store types: Farmers and Markets, Grocery Stores, Super Stores, and Supermarket. Specialty Store was excluded because it was mostly takeaway pizza outlets. It isn't used by the scripts here yet.

## Setup

This project uses [uv](https://docs.astral.sh/uv/) for Python package management.

```bash
# Install dependencies (creates/updates .venv automatically)
uv sync

# Install with dev dependencies
uv sync --group dev
```

## Usage

Run the scripts from the project root. They locate the project folder automatically. If you run them interactively (e.g. Jupyter), start from inside `02_code/`.

### 1. Fetch Overture Maps Data

Download food retail locations from Overture Maps for California (takes several minutes):

```bash
uv run python 02_code/01_fetch_overture.py
```

### 2. Create Stratified Sample

Generate a stratified sample for manual classification:

```bash
uv run python 02_code/02_create_sample.py
```

### 3. Create High-Confidence Grocery Dataset

Filter the full dataset down to likely grocery stores (no extra download):

```bash
uv run python 02_code/03_high_confidence_grocery.py
```

### 4. Manual Classification

See [CODEBOOK.md](CODEBOOK.md) for detailed coding instructions on how to classify stores using Virtual Ground Truthing.

## Development

```bash
# Run linting
uv run ruff check .

# Run formatting
uv run ruff format .
```

## License

MIT License - see [LICENSE](LICENSE) for details.
