# ============================================================
# Bologna Synthetic Population
# Data Processing Pipeline (FIXED VERSION)
# ============================================================

import pandas as pd
from pathlib import Path

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

DATA_INTERIM = Path("data/interim")
DATA_PROCESSED = Path("data/processed")

DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# Load datasets
# ------------------------------------------------------------

demographics = pd.read_csv(DATA_INTERIM / "demographics_clean.csv")
households = pd.read_csv(DATA_INTERIM / "households.csv")
activity = pd.read_csv(DATA_INTERIM / "destination_activity_2023.csv")
income = pd.read_csv(DATA_INTERIM / "income.csv")
spatial = pd.read_csv(DATA_INTERIM / "spatial_lookup.csv")

print("Datasets loaded:")
print("Demographics:", demographics.shape)
print("Households:", households.shape)
print("Activity:", activity.shape)
print("Income:", income.shape)
print("Spatial lookup:", spatial.shape)
print("-" * 50)

# ------------------------------------------------------------
# Clean area names
# ------------------------------------------------------------

def clean_area(series):
    return series.str.strip().str.lower()

demographics["area_name"] = clean_area(demographics["area_name"])
activity["area_name"] = clean_area(activity["area_name"])
income["area_name"] = clean_area(income["area_name"])
spatial["area_name"] = clean_area(spatial["area_name"])

# ------------------------------------------------------------
# Clean zona names
# ------------------------------------------------------------

def clean_zona(series):

    series = series.str.strip().str.lower()

    replacements = {
        "san ruffillo": "s. ruffillo",
        "san vitale": "s. vitale",
        "santa viola": "s. viola"
    }

    return series.replace(replacements)

households["zona_name"] = clean_zona(households["zona_name"])
spatial["zona_name"] = clean_zona(spatial["zona_name"])

# Remove homeless category
households = households[households["zona_name"] != "senza fissa dimora"]

# ------------------------------------------------------------
# Valid areas
# ------------------------------------------------------------

valid_areas = set(spatial["area_name"])

demographics = demographics[demographics["area_name"].isin(valid_areas)]
activity = activity[activity["area_name"].isin(valid_areas)]
income = income[income["area_name"].isin(valid_areas)]

print("After filtering valid areas:")
print("Demographics:", demographics.shape)
print("Activity:", activity.shape)
print("Income:", income.shape)
print("-" * 50)

# ------------------------------------------------------------
# Workers and students
# ------------------------------------------------------------

activity["workers"] = activity["n_workers_private"] + activity["n_workers_public"]

activity_area = activity[[
    "area_name",
    "workers",
    "n_workers_schools"
]].rename(columns={"n_workers_schools": "students_school"})

# ------------------------------------------------------------
# Population shares (zona → area)
# ------------------------------------------------------------

area_pop = demographics.groupby("area_name")["population"].sum().reset_index()

area_pop = area_pop.merge(
    spatial[["area_name", "zona_name"]],
    on="area_name",
    how="left"
)

zona_pop = area_pop.groupby("zona_name")["population"].sum().reset_index()
zona_pop = zona_pop.rename(columns={"population": "zona_population"})

area_pop = area_pop.merge(zona_pop, on="zona_name")

area_pop["population_share"] = (
    area_pop["population"] / area_pop["zona_population"]
)

# ------------------------------------------------------------
# Distribute households to areas
# ------------------------------------------------------------

households = households.merge(
    area_pop[["area_name", "zona_name", "population_share"]],
    on="zona_name",
    how="left"
)

households["households_area"] = (
    households["num_households"] * households["population_share"]
)

households_area = households[[
    "area_name",
    "household_type",
    "household_size",
    "households_area"
]].rename(columns={"households_area": "households"})

households_area = households_area.dropna(subset=["area_name"])

# ------------------------------------------------------------
# Save processed datasets
# ------------------------------------------------------------

demographics.to_csv(DATA_PROCESSED / "demographics_area.csv", index=False)
households_area.to_csv(DATA_PROCESSED / "households_area.csv", index=False)
activity_area.to_csv(DATA_PROCESSED / "activity_area.csv", index=False)
income.to_csv(DATA_PROCESSED / "income_area.csv", index=False)
spatial.to_csv(DATA_PROCESSED / "spatial_lookup.csv", index=False)

print("======================================")
print("Processing complete")
print("======================================")

print("Areas in households dataset:", households_area["area_name"].nunique())