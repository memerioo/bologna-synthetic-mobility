# Data Folder

This folder contains the raw, interim, processed, and synthetic datasets for the Bologna Synthetic Mobility project.
Raw, interim, and processed datasets are ignored due to their licence. However the sources(see below) and scripts for cleaning (src/data) are included.


## Raw
- `raw/spatial/aree_statistiche.geojson` — [Statistical areas of Bologna; comune di Bologna](https://opendata.comune.bologna.it/explore/dataset/aree-statistiche/information/) - 
- `raw/spatial/zone.geojson` — [Official zones of Bologna; comune di Bologna](https://opendata.comune.bologna.it/explore/dataset/zone-del-comune-di-bologna/export/?location=11,44.4887,11.33169&basemap=jawg.streets)
- `raw/demographics/demographics.csv` - [Popolazione residente; comune di Bologna](https://opendata.comune.bologna.it/explore/dataset/popolazione-residente-per-eta-sesso-cittadinanza-quartiere-zona-area-statistica-/export/?flg=it-it&utm_source=chatgpt.com&disjunctive.area_statistica&disjunctive.quartiere&disjunctive.zona&disjunctive.sesso&disjunctive.eta_grandi&disjunctive.eta&disjunctive.cittadinanza&sort=codice_area_statistica)
- `raw/households/households.csv` - [Famiglie residenti per tipologia](https://opendata.comune.bologna.it/explore/dataset/famiglie-residenti-per-tipologia-della-famiglia-dimensione-familiarenumero-compo/export/?disjunctive.quartiere&disjunctive.zona&disjunctive.tipologia_famiglia&disjunctive.dimensione_familiare&sort=anno)
- `raw/income/income.csv` - [Redditi per area statistica; comune di Bologna](https://opendata.comune.bologna.it/explore/dataset/redditi-per-area-statistica/export/?sort=-anno_reddito)
- `raw/occupation/graf poli.csv` [Dati Mobilita; Ufficio Statistiche Bologna](https://public.tableau.com/app/profile/ufficio.statistiche.territoriali.bologna/viz/Dati_Mobilita_Comune_Bologna2023/Volumispostamenti)


## Interim
- `interim/spatial_lookup.csv` 
- `interim/demographics_clean.csv`
- `interim/destination_activity_2023.csv`
- `interim/households.csv`
- `interim/income.csv`

## Processed
- `processed/spatial_lookup.csv`
- `processed/demographics_area.csv`
- `processed/households_area.csv`
- `processed/income_area.csv`
- `processed/activity_area.csv`

