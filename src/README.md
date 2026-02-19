# Scripts Folder

This folder contains Python scripts for processing and preparing datasets for the Bologna Synthetic Mobility project.

## `data/spatial_lookup.py`
- Loads the raw spatial GeoJSON files (`aree_statistiche.geojson` and `zone.geojson`).
- Cleans and renames columns for consistency.
- Ensures both GeoDataFrames share the same CRS.
- Validates the area-to-zone mapping using spatial overlay (intersection-based), resolving mismatches.
- Produces the interim lookup table (`data/interim/spatial_lookup.csv`) with columns:
  - `area_id`, `area_name`, `zona_id`, `zona_name`, `quartiere_id`, `quartiere_name`.

## Other scripts
- Add descriptions here for any other scripts you create.

