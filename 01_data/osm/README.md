# OpenStreetMap

| File | Made by | Contents |
|---|---|---|
| `california-latest.osm.pbf` | `02_code/01c_fetch_osm.py` | Statewide California extract from [Geofabrik](https://download.geofabrik.de/north-america/us/california.html). About 1 GB, so it is **git-ignored** |
| `california-latest.metadata.json` | same script | Download date, Last-Modified, size and MD5 of the extract you have locally (committed) |

The ADU paper routed on a smaller BBBike Sacramento extract (`data/raw/05_gis/r5_network_sac/Sacramento.osm.pbf`, 28 MB, downloaded 30 August 2026; covers -121.63 to -121.15 lon, 38.37 to 38.74 lat). That file stays in the ADU package. Geofabrik and BBBike both overwrite their extracts, so archive whichever `.pbf` a paper uses outside git.
