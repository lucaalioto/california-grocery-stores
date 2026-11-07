"""
01b_fetch_snap.py
Downloads every SNAP-authorized retailer in California from the USDA FNS
SNAP Retailer Locator and saves it to 01_data/snap/.

The locator is backed by a public ArcGIS feature layer. The layer caps each
response at a few thousand rows, so this pages through with resultOffset.

NOTE: the layer URL and the state field name below were written without
network access to check them. If the request fails or returns 0 rows,
open the Retailer Locator, find the layer URL in the browser's network tab,
and update SNAP_LAYER_URL / STATE_FIELD. A manual fallback is described in
01_data/snap/README.md.

Output: 01_data/snap/snap_retailers_california_<YYYY-MM-DD>.csv (all store types;
filter by Store_Type downstream rather than at download time).
"""

import datetime as dt
import json
import os
import urllib.parse
import urllib.request

import pandas as pd

SNAP_LAYER_URL = (
    "https://services1.arcgis.com/RLQu0rK7h4kbsBq5/arcgis/rest/services/"
    "snap_retailer_location_data/FeatureServer/0/query"
)
STATE_FIELD = "State"
PAGE_SIZE = 2000


def project_root():
    try:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    except NameError:
        return os.path.abspath(os.path.join(os.getcwd(), ".."))


def fetch_page(offset):
    params = {
        "where": f"{STATE_FIELD}='CA'",
        "outFields": "*",
        "returnGeometry": "false",
        "orderByFields": "ObjectId",
        "resultOffset": offset,
        "resultRecordCount": PAGE_SIZE,
        "f": "json",
    }
    url = f"{SNAP_LAYER_URL}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=120) as resp:
        data = json.load(resp)
    if "error" in data:
        raise RuntimeError(f"ArcGIS error: {data['error']}")
    return data


def main():
    out_dir = os.path.join(project_root(), "01_data", "snap")
    os.makedirs(out_dir, exist_ok=True)

    rows, offset = [], 0
    while True:
        data = fetch_page(offset)
        feats = data.get("features", [])
        rows.extend(f["attributes"] for f in feats)
        print(f"  fetched {len(rows):,} rows")
        if not feats or not data.get("exceededTransferLimit"):
            break
        offset += len(feats)

    if not rows:
        raise SystemExit("No rows returned; check SNAP_LAYER_URL and STATE_FIELD.")

    df = pd.DataFrame(rows)
    today = dt.date.today().isoformat()
    out = os.path.join(out_dir, f"snap_retailers_california_{today}.csv")
    df.to_csv(out, index=False)
    print(f"Saved {len(df):,} California SNAP retailers to {out}")
    for col in ("Store_Type", "Store Type"):
        if col in df.columns:
            print(df[col].value_counts().to_string())
            break


if __name__ == "__main__":
    main()
