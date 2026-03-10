import pandas as pd
from pathlib import Path
import numpy as np

# Paths
DATA_PROCESSED = Path("data/processed")
DATA_CONSTRAINTS = Path("data/constraints")
DATA_CONSTRAINTS.mkdir(parents=True, exist_ok=True)

# Load cleaned datasets
households_area = pd.read_csv(DATA_PROCESSED / "households_area.csv")
demographics_area = pd.read_csv(DATA_PROCESSED / "demographics_area.csv")
activity_area = pd.read_csv(DATA_PROCESSED / "activity_area.csv")
income_area = pd.read_csv(DATA_PROCESSED / "income_area.csv")

# ------------------------------------------------------------
# Round household counts up
# ------------------------------------------------------------
households_area["households"] = np.ceil(households_area["households"]).astype(int)

# Save rounded households as constraint
households_area.to_csv(DATA_CONSTRAINTS / "households_area_constraints.csv", index=False)
print("Household constraints saved.")


# Population constraints per area
population_constraints = demographics_area.groupby("area_name")["population"].sum().reset_index()
population_constraints = population_constraints.rename(columns={"population": "total_population"})

population_constraints.to_csv(DATA_CONSTRAINTS / "population_area_constraints.csv", index=False)
print("Population constraints saved.")

# Workers and students constraints
work_student_constraints = activity_area.copy()
work_student_constraints.to_csv(DATA_CONSTRAINTS / "work_student_area_constraints.csv", index=False)
print("Worker and student constraints saved.")


# Example: 30% of population have bike access (placeholder)
bike_constraints = population_constraints.copy()
bike_constraints["bike_access_fraction"] = 0.3  # placeholder, can be refined later

bike_constraints.to_csv(DATA_CONSTRAINTS / "bike_access_constraints.csv", index=False)
print("Bike access constraints saved.")