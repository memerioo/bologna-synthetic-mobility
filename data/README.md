# Data Folder

This folder contains the raw, interim, and processed datasets for the Bologna Synthetic Mobility project.

## Raw
- `raw/spatial/aree_statistiche.geojson` — Statistical areas of Bologna
- `raw/spatial/zone.geojson` — Official zones of Bologna
- Other raw datasets: demographics, income, households, occupation

## Interim
- `interim/spatial_lookup.csv` — Spatial lookup table generated from `aree_statistiche.geojson` and `zone.geojson`
- Maps each area to its validated `zona_id`, `zona_name`, `quartiere_id`, and `quartiere_name`.
