import pandas as pd

# Load raw income data
df = pd.read_csv(
    "data/raw/income/income.csv",
    sep=";",          
    encoding="utf-8"  
)

# Clean column names
df.columns = df.columns.str.replace("\ufeff", "", regex=False)
df.columns = df.columns.str.strip()

# Rename columns to standard names
df = df.rename(columns={
    "Anno reddito": "year",
    "Area Statistica": "area_name",
    "N contribuenti": "n_taxpayers",
    "Reddito imponibile ai fini irpef": "taxable_income_irpef",
    "Reddito imponibile ai fini dell'addizionale irpef": "taxable_income_additional",
    "Reddito medio contribuente": "average_income"
})

# Keep only latest year
latest_year = df["year"].max()
df = df[df["year"] == latest_year].copy()

# Keep only necessary columns
df = df[
    ["area_name", "n_taxpayers", "taxable_income_irpef", 
     "taxable_income_additional", "average_income"]
]

print("Rows after filtering latest year:", len(df))
print("Year kept:", latest_year)
print("\nHead:\n", df.head())
print(df.info())

# Save cleaned dataset
df.to_csv("data/interim/income.csv", index=False)
print("\nSaved: data/interim/income.csv")