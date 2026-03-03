import pandas as pd

# Load CSV
df = pd.read_csv(
    "data/raw/occupation/occupation.csv",
    sep=";",
    encoding="utf-8"
)

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

# -------------------------------------------------
# Keep LAST TWO YEARS because of COVID, we will check inconsistencies in notebooks before final cleaning.
# -------------------------------------------------

df['year'] = pd.to_numeric(df['year'], errors='coerce')

latest_year = df['year'].max()
second_latest_year = sorted(df['year'].unique())[-2]

print("Latest year:", latest_year)
print("Second latest year:", second_latest_year)

df = df[df['year'].isin([second_latest_year, latest_year])].copy()

print("Rows after filtering last two years:", len(df))
print("Years kept:", df['year'].unique())

# -------------------------------------------------

# Fill missing numeric values
df['n_workers_public'] = df['n_workers_public'].fillna(0).astype(int)
df['n_students'] = df['n_students'].fillna(0).astype(int)

# Keep relevant columns (NOW INCLUDING year)
df = df[
    [
        'year',
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
df.to_csv("data/interim/occupation_2years.csv", index=False)

print("\nCleaned occupation dataset (2 years) saved.")