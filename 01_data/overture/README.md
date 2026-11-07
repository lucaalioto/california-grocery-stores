# Overture Maps

Source: [Overture Maps](https://overturemaps.org) **places** theme, read straight from `s3://overturemaps-us-west-2` with DuckDB.

| File | Made by | Release | Contents |
|---|---|---|---|
| `california_food_retail_full.{parquet,csv,dta}` | `02_code/01_fetch_overture.py` | `2025-12-17.0` | Every California place whose primary category is `grocery_store`, `supermarket`, `convenience_store` or `specialty_food_store`, or whose alternate categories include `grocery_store`, `supermarket` or `convenience_store` (43,521 rows) |
| `adu_sacramento_2026-02-18.0/sacramento_grocery_stores.{csv,parquet}` | ADU replication package, `code/03_grocery_data.py` | `2026-02-18.0` | Frozen copy of the 365 Sacramento stores used in the ADU paper (primary category `supermarket` or `grocery_store`, minus convenience/gas alternates, inside -121.63 to -121.03 lon, 38.02 to 38.74 lat) |

Overture keeps only its latest few releases online, so neither release above can be downloaded again. That is why the ADU copy is kept here: it is the only record of the exact stores the paper used. Re-running script 01 now pulls the release pinned in the script and gives different data.
