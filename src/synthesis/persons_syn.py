# ============================================================
# Bologna Synthetic Population
# Individual Generation (Improved)
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------
DATA_PROCESSED = Path("data/processed")
OUTPUT_PATH = Path("data/synthetic")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# Load datasets
# ------------------------------------------------------------
households = pd.read_csv(OUTPUT_PATH / "households_synthetic.csv")
demographics = pd.read_csv(DATA_PROCESSED / "demographics_area.csv")
activity = pd.read_csv(DATA_PROCESSED / "activity_area.csv")
income = pd.read_csv(DATA_PROCESSED / "income_area.csv")

for df in [households, demographics, activity, income]:
    df["area_name"] = df["area_name"].str.strip().str.lower()

# ------------------------------------------------------------
# Expand demographics into individuals
# ------------------------------------------------------------
def expand_demographics(df):
    records = []
    for _, row in df.iterrows():
        for _ in range(int(row["population"])):
            records.append({
                "area_name": row["area_name"],
                "sex": row["sex"],
                "age_group": row["age_group"],
                "citizenship": row["citizenship"]
            })
    return pd.DataFrame(records)

dem_people = expand_demographics(demographics)
dem_people = dem_people.sample(frac=1).reset_index(drop=True)

# ------------------------------------------------------------
# Age group midpoints (for income modeling)
# ------------------------------------------------------------
age_mid = {
    "02 e prima": 2,
    "03-05": 4,
    "06-14": 10,
    "15-24": 20,
    "25-34": 30,
    "35-44": 40,
    "45-54": 50,
    "55-64": 60,
    "65 e oltre": 70
}

# ------------------------------------------------------------
# Allowed employment states
# ------------------------------------------------------------
def allowed_status(age_group):

    if age_group in ["02 e prima", "03-05"]:
        return (0,0)

    if age_group == "06-14":
        return (0,1)

    if age_group == "15-24":
        return (1,1)

    if age_group in ["25-34","35-44","45-54","55-64"]:
        return (1,0)

    return (0,0)

# ------------------------------------------------------------
# Income generator
# ------------------------------------------------------------
def generate_income(age_group, worker, student, area_avg):

    age = age_mid.get(age_group,30)

    if age < 16:
        return 0

    if worker and student:

        base = area_avg * 0.45
        return max(0,np.random.normal(base, base*0.25))

    if student and not worker:

        if np.random.rand() < 0.75:
            return 0

        base = area_avg * 0.25
        return max(0,np.random.normal(base, base*0.30))

    if worker:

        if age < 30:
            multiplier = 0.75
        elif age < 40:
            multiplier = 1.0
        elif age < 55:
            multiplier = 1.15
        else:
            multiplier = 0.9

        base = area_avg * multiplier
        return max(0,np.random.normal(base, base*0.20))

    if age >= 65:

        base = area_avg * 0.55
        return max(0,np.random.normal(base, base*0.20))

    return 0


# ------------------------------------------------------------
# Activity quotas per area
# ------------------------------------------------------------
activity_quota = activity.set_index("area_name")[["workers","students_school"]].to_dict("index")

area_remaining = {
    a:{
        "workers":int(v["workers"]),
        "students":int(v["students_school"])
    }
    for a,v in activity_quota.items()
}

# ------------------------------------------------------------
# Generate persons
# ------------------------------------------------------------
persons=[]
person_counter=1

for _,hh in households.iterrows():

    area = hh["area_name"]
    hh_size = int(hh["household_size"])
    hh_id = hh["household_id"]

    dem_area = dem_people[dem_people["area_name"]==area]

    if len(dem_area)<hh_size:
        sampled = dem_area.sample(n=hh_size,replace=True)
    else:
        sampled = dem_area.sample(n=hh_size,replace=False)

    avg_income = income.loc[income["area_name"]==area,"average_income"]
    area_avg = float(avg_income.values[0]) if len(avg_income)>0 else 30000

    for _,p in sampled.iterrows():

        age_group = p["age_group"]
        allow_worker,allow_student = allowed_status(age_group)

        worker=0
        student=0

        if allow_worker and area_remaining[area]["workers"]>0:
            worker=1
            area_remaining[area]["workers"]-=1

        if allow_student and area_remaining[area]["students"]>0:
            student=1
            area_remaining[area]["students"]-=1

        income_val = generate_income(age_group,worker,student,area_avg)

        persons.append({
            "person_id":f"P_{person_counter:08d}",
            "household_id":hh_id,
            "area_name":area,
            "sex":p["sex"],
            "age_group":age_group,
            "citizenship":p["citizenship"],
            "worker":worker,
            "student":student,
            "income":round(income_val,2)
        })

        person_counter+=1

        if person_counter%1000==0:
            print(f"Generated {person_counter} individuals")

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------
persons_df = pd.DataFrame(persons)

output_file = OUTPUT_PATH / "persons_synthetic.csv"
persons_df.to_csv(output_file,index=False)

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------
print("======================================")
print("Synthetic Individual Generation Finished")
print("======================================")

print(f"Total persons: {len(persons_df)}")
print(f"Households: {households['household_id'].nunique()}")
print(f"Workers: {persons_df['worker'].sum()}")
print(f"Students: {persons_df['student'].sum()}")
print(f"Average income: {persons_df['income'].mean():.0f}")

print(f"Saved to {output_file}")