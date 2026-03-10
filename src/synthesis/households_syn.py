# ============================================================
# Bologna Synthetic Population
# Household Generation
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------
DATA_PROCESSED = Path("data/processed")
OUTPUT_PATH = Path("data/synthetic")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# Load cleaned households data
# ------------------------------------------------------------
households_area = pd.read_csv(DATA_PROCESSED / "households_area.csv")

# ------------------------------------------------------------
# Round household counts up
# ------------------------------------------------------------
households_area["households"] = np.ceil(households_area["households"]).astype(int)

# ------------------------------------------------------------
# Function: convert household size category to numeric value
# ------------------------------------------------------------
def hh_size_to_int(hh_size):

    hh_size = str(hh_size)

    if hh_size == "Oltre 10":
        return np.random.randint(11, 16)   # 11–15

    elif hh_size == "6-10":
        return np.random.randint(6, 11)    # 6–10

    else:
        return int(hh_size)

# ------------------------------------------------------------
# Generate synthetic households
# ------------------------------------------------------------
synthetic_households = []

household_counter = 1

for area in households_area["area_name"].unique():

    hh_area = households_area[households_area["area_name"] == area]

    for _, row in hh_area.iterrows():

        hh_count = int(row["households"])
        hh_size_cat = str(row["household_size"])

        for _ in range(hh_count):

            hh_size = hh_size_to_int(hh_size_cat)

            synthetic_households.append({

                "household_id": f"HH_{household_counter:07d}",
                "area_name": area,
                "household_size_cat": hh_size_cat,
                "household_size": hh_size

            })

            household_counter += 1

# ------------------------------------------------------------
# Create dataframe
# ------------------------------------------------------------
synthetic_df = pd.DataFrame(synthetic_households)

# ------------------------------------------------------------
# Save synthetic households
# ------------------------------------------------------------
output_file = OUTPUT_PATH / "households_synthetic.csv"
synthetic_df.to_csv(output_file, index=False)

# ------------------------------------------------------------
# Print summary
# ------------------------------------------------------------
print("======================================")
print("Synthetic Household Generation Finished")
print("======================================")
print(f"Total households generated: {len(synthetic_df)}")
print(f"Total synthetic population: {synthetic_df['household_size'].sum()}")
print(f"Saved to: {output_file}")