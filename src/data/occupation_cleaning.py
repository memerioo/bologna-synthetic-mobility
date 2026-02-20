import pandas as pd

# Load CSV
df = pd.read_csv(
    "data/raw/occupation/occupation.csv",
    sep=";",          # likely ; like others
    encoding="utf-8"  # safe default
)

# Quick inspection
print("Columns:\n", df.columns.tolist())
print("\nShape:", df.shape)
print("\nHead:\n", df.head())
print("\nInfo:")
print(df.info())

# Clean column names
df.columns = df.columns.str.replace("\ufeff", "", regex=False)
df.columns = df.columns.str.strip()
df = df.rename(columns={
    'Sezione censimento (2011)': 'census_section',
    'Anno di riferimento': 'year',
    'Nome quartiere': 'quartiere_name',
    'Nome zona': 'zona_name',
    'Nome area': 'area_name',
    'Numero unità locali': 'n_local_units',
    'Numero addetti (dipendenti e indipendenti)': 'n_workers_private',
    'Numero addetti istituzioni pubbliche': 'n_workers_public',
    'Numero studenti': 'n_students'
})

# Keep only latest year
latest_year = df['year'].max()
df = df[df['year'] == latest_year].copy()
print("Rows after filtering latest year:", len(df))
print("Year kept:", latest_year)

# Optional: fill missing with 0
df['n_workers_public'] = df['n_workers_public'].fillna(0).astype(int)
df['n_students'] = df['n_students'].fillna(0).astype(int)

# Keep only relevant columns
df = df[
    [
        'area_name',
        'quartiere_name',
        'zona_name',
        'census_section',
        'n_local_units',
        'n_workers_private',
        'n_workers_public',
        'n_students'
    ]
]

print("\nHead:\n", df.head())
print(df.info())


# Save cleaned dataset
df.to_csv("data/interim/occupation.csv", index=False)
print("\nCleaned occupation dataset saved to data/interim/occupation.csv")
