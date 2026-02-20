import pandas as pd

# Load
df = pd.read_csv(
    "data/raw/households/households.csv",
    sep=";",
    encoding="utf-8"
)

# Clean column names
df.columns = df.columns.str.replace("\ufeff", "", regex=False)
df.columns = df.columns.str.strip()

print("Columns:")
print(df.columns.tolist())

print("\nShape:", df.shape)
print("\nHead:")
print(df.head())

print("\nInfo:")
print(df.info())

print("\nYears available:")
print(sorted(df["Anno"].unique()))

print("\nRows per year:")
print(df["Anno"].value_counts().sort_index())

total_people = df[df["Anno"] == 2024]["Componenti"].sum()
print("Total people 2024:", total_people)

# Keep only latest year
df_2024 = df[df["Anno"] == 2024].copy()

# Clean column names
df_2024 = df_2024.rename(columns={
    "Quartiere": "quartiere_name",
    "Zona": "zona_name",
    "Tipologia Famiglia": "household_type",
    "Dimensione Familiare": "household_size",
    "Numero Famiglie": "num_households",
    "Componenti": "population"
})

# Keep only useful columns
df_2024 = df_2024[
    [
        "quartiere_name",
        "zona_name",
        "household_type",
        "household_size",
        "num_households",
        "population"
    ]
]

# Save cleaned dataset
df_2024.to_csv("data/interim/households.csv", index=False)
print("Saved → data/interim/households.csv")
