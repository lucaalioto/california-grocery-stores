# SNAP retailers (USDA FNS)

Source: [USDA FNS SNAP Retailer Locator](https://usda-fns.maps.arcgis.com/apps/webappviewer/index.html?id=15e1c457b56c4a729861d015cd626a23).

| File | Made by | Pulled | Contents |
|---|---|---|---|
| `snap_retailers_sacramento_2026-04.csv` | Manual export from the locator | April 2026 | Sacramento, Yolo, Placer and Solano counties, pre-filtered on the website to Farmers and Markets, Grocery Stores, Super Stores and Supermarket (419 retailers). Same file the ADU paper used (`data/raw/04_merge/SNAP Retailer Location data.csv`, identical MD5) |
| `snap_retailers_california_<date>.csv` | `02_code/01b_fetch_snap.py` | not yet run | Every SNAP-authorized retailer in California, all store types |

Specialty Store was left out of the Sacramento export because it was mostly takeaway pizza. The statewide pull keeps every store type so that choice can be made, and documented, in code.

**Manual fallback** if the script's layer URL is wrong: FNS also publishes a national historical retailer file (every retailer ever authorized, with authorization and end dates) at <https://www.fns.usda.gov/snap/retailer/historical-data>. Download it, filter to `State == "CA"` and to retailers with no end date, and save it here with the pull date in the name.
