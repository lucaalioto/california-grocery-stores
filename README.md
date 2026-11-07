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
├── 01_data/                              # Raw inputs, one folder per source (see Data below)
│   ├── overture/                         # Overture Maps places
│   ├── snap/                             # USDA SNAP retailers
│   └── osm/                              # OpenStreetMap extract (.pbf is git-ignored)
├── 02_code/
│   ├── 01_fetch_overture.py              # Overture food retail for California -> 01_data/overture/
│   ├── 01b_fetch_snap.py                 # SNAP retailers for California -> 01_data/snap/
│   ├── 01c_fetch_osm.py                  # OSM California extract -> 01_data/osm/
│   ├── 02_create_sample.py               # Stratified sample for manual coding -> 03_output/
│   └── 03_high_confidence_grocery.py     # High-confidence grocery subset -> 03_output/
├── 03_output/                            # Datasets derived from 01_data
├── CODEBOOK.md                           # Coding instructions for classification
├── pyproject.toml                        # Project configuration
├── uv.lock                               # Pinned package versions
└── README.md                             # This file
```

## Data

The project uses the same three sources as the ADU replication package, each in its own folder under `01_data/` with a README giving provenance, release or pull date, and coverage. All three are meant to be statewide (California).

| Source | Folder | Statewide file | Status |
|---|---|---|---|
| Overture Maps places | `01_data/overture/` | `california_food_retail_full.*` (43,521 places, release `2025-12-17.0`) | In repo. Also holds a frozen copy of the 365 Sacramento stores the ADU paper used (release `2026-02-18.0`) |
| USDA SNAP retailers | `01_data/snap/` | `snap_retailers_california_<date>.csv` | Run `01b_fetch_snap.py`. Only the Sacramento-region export used by the ADU paper is in the repo so far |
| OpenStreetMap | `01_data/osm/` | `california-latest.osm.pbf` | Run `01c_fetch_osm.py`. About 1 GB, so it is git-ignored; only its metadata file is committed |

Derived datasets in `03_output/`:

| File | Script | Contents |
|------|--------|----------|
| `california_manual_coding_sample.csv` | 02 | Stratified random sample of 200 locations (100 with a website, 100 without; seed 42) with blank coding columns |
| `california_grocery_stores.{parquet,csv,dta}` | 03 | High-confidence subset: primary category `supermarket` or `grocery_store`, excluding anything also tagged `convenience_store`, `gas_station`, `petrol_station`, or `fuel_station`. Not included; run script 03 to create it |

> **Release note:** Overture only keeps its most recent releases online and deletes older ones. Neither `2025-12-17.0` nor `2026-02-18.0` can be downloaded again, so `01_fetch_overture.py` is pinned to **`2026-09-23.1`**. Re-running script 01 (and then 02) will produce different data and a different random sample. If the pinned release has also been removed, update `release` in `01_fetch_overture.py` to a current one ([release list](https://docs.overturemaps.org/release/latest/)).

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

### 1. Fetch the raw data

Download food retail locations from Overture Maps for California (takes several minutes):

```bash
uv run python 02_code/01_fetch_overture.py
```

Download California SNAP retailers and the California OpenStreetMap extract:

```bash
uv run python 02_code/01b_fetch_snap.py
uv run python 02_code/01c_fetch_osm.py
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
