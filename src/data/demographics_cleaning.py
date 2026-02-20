import pandas as pd

df = pd.read_csv(
    "data/raw/demographics/demographics.csv",
    sep=";",          # 👈 important
    encoding="utf-8"  # safe default
)

# Clean column names (remove BOM and strip spaces)
df.columns = df.columns.str.replace("\ufeff", "", regex=False)
df.columns = df.columns.str.strip()


print(df.columns.tolist())


# Keep only latest year
df = df[df["Anno"] == 2024].copy()

# Clean column names
df = df.rename(columns={
    "Codice Area Statistica": "area_id",
    "Area Statistica": "area_name",
    "Quartiere": "quartiere_name",
    "Zona": "zona_name",
    "Sesso": "sex",
    "Età grandi": "age_group",
    "Cittadinanza": "citizenship",
    "Residenti": "population"
})

# Keep only needed columns
df = df[
    [
        "area_id",
        "area_name",
        "quartiere_name",
        "zona_name",
        "sex",
        "age_group",
        "citizenship",
        "population",
    ]
]


print("Rows after filtering 2024:", len(df))


print("\nUnique sexes:", df["sex"].unique())
print("Unique citizenship:", df["citizenship"].unique())
print("Unique age groups:", df["age_group"].unique()[:10])
print("Total population 2024:", df["population"].sum())


print(df.head())
print(df.columns)
print(df.info())


df.to_csv("data/interim/demographics_clean.csv", index=False)

print("Saved to: data/interim/demographics_clean.csv")
