from pathlib import Path
import geopandas as gpd

RAW_DIR = Path("data/raw/spatial")
INTERIM_DIR = Path("data/interim")


def load_data():
    print("Loading geojson files...")
    aree = gpd.read_file(RAW_DIR / "aree_statistiche.geojson")
    zone = gpd.read_file(RAW_DIR / "zone.geojson")
    return aree, zone


def clean_columns(aree, zone):
    print("Cleaning columns...")
    aree = aree.rename(columns={
        "codice_area_statistica": "area_id",
        "area_statistica": "area_name",
        "cod_zona": "zona_id_declared",
        "zona": "zona_name_declared",
        "cod_quar": "quartiere_id",
        "quartiere": "quartiere_name"
    })
    zone = zone.rename(columns={
        "codzona": "zona_id",
        "nomezona": "zona_name"
    })
    return aree, zone


def ensure_crs(aree, zone):
    # use projected CRS for accurate area calculations
    projected_crs = "EPSG:32632"  # UTM zone 32N for Bologna
    aree = aree.to_crs(projected_crs)
    zone = zone.to_crs(projected_crs)
    return aree, zone


def validate_zones(aree, zone):
    print("Validating spatial hierarchy (intersection based)...")

    # overlay (intersection)
    joined = gpd.overlay(aree, zone, how="intersection")

    # after overlay, rename automatically created columns
    # geopandas adds suffixes if needed: check what exists
    area_cols = [c for c in joined.columns if c.endswith("_area")]
    zone_cols = [c for c in joined.columns if c in ["zona_id", "zona_name"]]

    # compute intersection area
    joined["overlap_area"] = joined.geometry.area

    # keep the biggest overlap per area
    best_match = joined.sort_values("overlap_area", ascending=False).drop_duplicates(subset="area_id")

    # merge back to original aree
    result = aree.merge(
        best_match[["area_id", "zona_id", "zona_name"]],
        on="area_id",
        how="left"
    )

    mismatches = result[result["zona_id_declared"] != result["zona_id"]]

    print(f"Total areas: {len(result)}")
    print(f"Mismatched zones after spatial correction: {len(mismatches)}")

    if len(mismatches) > 0:
        print("\nExample mismatches:")
        print(mismatches[[
            "area_id",
            "area_name",
            "zona_id_declared",
            "zona_id"
        ]].head())

    # trust spatial hierarchy
    result["zona_name"] = result["zona_name"]

    return result


def build_lookup(df):
    print("Building lookup table...")
    lookup = df[[
        "area_id",
        "area_name",
        "zona_id",
        "zona_name",
        "quartiere_id",
        "quartiere_name"
    ]].drop_duplicates()
    lookup = lookup.sort_values("area_id").reset_index(drop=True)
    return lookup


def save_lookup(lookup):
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    output = INTERIM_DIR / "spatial_lookup.csv"
    lookup.to_csv(output, index=False)
    print(f"Saved → {output}")


def main():
    aree, zone = load_data()
    aree, zone = clean_columns(aree, zone)
    aree, zone = ensure_crs(aree, zone)
    joined = validate_zones(aree, zone)
    lookup = build_lookup(joined)
    save_lookup(lookup)


if __name__ == "__main__":
    main()
