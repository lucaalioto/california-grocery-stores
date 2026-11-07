"""
01c_fetch_osm.py
Downloads the statewide California OpenStreetMap extract from Geofabrik and
saves it to 01_data/osm/.

The .pbf is about 1 GB, too large for GitHub, so it is git-ignored. The
script writes a small metadata file (download date, size, MD5) that IS
committed, so every analysis can record which extract it used. Geofabrik
regenerates the extract daily and does not keep old ones, so keep the
.pbf you used for a paper somewhere permanent (e.g. OneDrive or Zenodo).

Output:
    01_data/osm/california-latest.osm.pbf        (ignored by git)
    01_data/osm/california-latest.metadata.json  (committed)
"""

import datetime as dt
import hashlib
import json
import os
import urllib.request

OSM_URL = "https://download.geofabrik.de/north-america/us/california-latest.osm.pbf"


def project_root():
    try:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    except NameError:
        return os.path.abspath(os.path.join(os.getcwd(), ".."))


def main():
    out_dir = os.path.join(project_root(), "01_data", "osm")
    os.makedirs(out_dir, exist_ok=True)
    pbf = os.path.join(out_dir, "california-latest.osm.pbf")

    print(f"Downloading {OSM_URL} (about 1 GB)...")
    md5 = hashlib.md5()
    with urllib.request.urlopen(OSM_URL, timeout=600) as resp, open(pbf, "wb") as fh:
        last_modified = resp.headers.get("Last-Modified")
        while chunk := resp.read(1 << 20):
            fh.write(chunk)
            md5.update(chunk)

    meta = {
        "source": OSM_URL,
        "downloaded": dt.date.today().isoformat(),
        "last_modified": last_modified,
        "bytes": os.path.getsize(pbf),
        "md5": md5.hexdigest(),
    }
    with open(os.path.join(out_dir, "california-latest.metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
    print(f"Saved {pbf} ({meta['bytes'] / 1e9:.2f} GB, md5 {meta['md5']})")


if __name__ == "__main__":
    main()
