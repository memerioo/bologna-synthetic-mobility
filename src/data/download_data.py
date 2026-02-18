from pathlib import Path
import requests

# Base folder for raw data
RAW_DATA_DIR = Path("data/raw")

# All datasets, grouped by folder and with clean filenames
DATASETS = {
    "demographics": {
        "demographics.csv": "https://opendata.comune.bologna.it/explore/dataset/popolazione-residente-per-eta-sesso-cittadinanza-quartiere-zona-area-statistica-/download/?format=csv&timezone=Europe/Rome&lang=it&use_labels_for_header=true&csv_separator=;"
    },
    "households": {
        "households.csv": "https://opendata.comune.bologna.it/explore/dataset/famiglie-residenti-per-tipologia-della-famiglia-dimensione-familiarenumero-compo/download/?format=csv&timezone=Europe/Rome&lang=it&use_labels_for_header=true&csv_separator=;"
    },
    "income": {
        "income.csv": "https://opendata.comune.bologna.it/explore/dataset/redditi-per-area-statistica/download/?format=csv&timezone=Europe/Rome&lang=it&use_labels_for_header=true&csv_separator=;"
    },
    "occupation": {
        "occupation.csv": "https://opendata.comune.bologna.it/explore/dataset/occupati_statistica/download/?format=csv&timezone=Europe/Rome&lang=it&use_labels_for_header=true&csv_separator=;"
    },
    "spatial": {
        "aree_statistiche.geojson": "https://opendata.comune.bologna.it/explore/dataset/aree-statistiche/download/?format=geojson",
        "zone.geojson": "https://opendata.comune.bologna.it/explore/dataset/zone-del-comune-di-bologna/download/?format=geojson"
    },
}


def download_file(folder: Path, filename: str, url: str):
    """Download a single file into the appropriate folder."""
    output_path = folder / filename
    if output_path.exists():
        print(f"{filename} already exists in {folder}, skipping.")
        return

    print(f"Downloading {filename} into {folder}...")
    response = requests.get(url)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)

    print(f"Saved {filename} to {output_path}")


def main():
    for folder_name, files in DATASETS.items():
        folder_path = RAW_DATA_DIR / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)

        for filename, url in files.items():
            download_file(folder_path, filename, url)


if __name__ == "__main__":
    main()
