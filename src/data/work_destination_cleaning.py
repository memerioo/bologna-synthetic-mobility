import pandas as pd

# -------------------------------------------------
# File paths
# -------------------------------------------------

INPUT_PATH = "data/raw/occupation/graf poli.csv"
OUTPUT_PATH = "data/interim/destination_activity_2023.csv"

# -------------------------------------------------
# Load raw file
# -------------------------------------------------
# - UTF-16 encoding (ISTAT style)
# - Tab-separated
# - Skip fake header row
# -------------------------------------------------

df = pd.read_csv(
    INPUT_PATH,
    sep="\t",
    encoding="utf-16",
    skiprows=1
)

print("Raw shape:", df.shape)
print("\nRaw preview:")
print(df.head())

# -------------------------------------------------
# Rename columns properly
# -------------------------------------------------

df.columns = [
    "area_name",
    "n_workers_public",
    "n_workers_private",
    "n_workers_schools"
]

# -------------------------------------------------
# Clean numeric columns
# -------------------------------------------------

numeric_cols = [
    "n_workers_public",
    "n_workers_private",
    "n_workers_schools"
]

for col in numeric_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)  # remove thousands separator
        .str.strip()
    )

    df[col] = pd.to_numeric(df[col], errors="coerce")  # invalid → NaN
    df[col] = df[col].fillna(0).astype(int)            # NaN → 0 safely

# -------------------------------------------------
# Clean area names
# -------------------------------------------------

df["area_name"] = df["area_name"].astype(str).str.strip()

# Drop rows where area_name is empty
df = df[df["area_name"] != ""]

# -------------------------------------------------
# Add reference year
# -------------------------------------------------

df["year"] = 2023

# -------------------------------------------------
# Reorder columns
# -------------------------------------------------

df = df[
    [
        "year",
        "area_name",
        "n_workers_private",
        "n_workers_public",
        "n_workers_schools"
    ]
]

# -------------------------------------------------
# Final checks
# -------------------------------------------------

print("\nCleaned dataset info:")
print(df.info())

print("\nSummary totals:")
print(df[numeric_cols].sum())

# -------------------------------------------------
# Save cleaned dataset
# -------------------------------------------------

df.to_csv(OUTPUT_PATH, index=False)

print(f"\n Cleaned dataset saved to: {OUTPUT_PATH}")