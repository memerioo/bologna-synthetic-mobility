# ============================================================
# Bologna Synthetic Population
# Mobility Assignment (Cars & Bikes)
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------
DATA_SYNTH = Path("data/synthetic")

persons_file = DATA_SYNTH / "persons_synthetic.csv"
households_file = DATA_SYNTH / "households_synthetic.csv"


# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------
print("Loading datasets...")

persons = pd.read_csv(persons_file)
households = pd.read_csv(households_file)

print("Persons:", len(persons))
print("Households:", len(households))


# ------------------------------------------------------------
# Age midpoints
# ------------------------------------------------------------
age_mid = {
    "02 e prima":2,
    "03-05":4,
    "06-14":10,
    "15-24":20,
    "25-34":30,
    "35-44":40,
    "45-54":50,
    "55-64":60,
    "65 e oltre":70
}

persons["age"] = persons["age_group"].map(age_mid)


# ------------------------------------------------------------
# Household Income (safe for reruns)
# ------------------------------------------------------------
print("\nCalculating household incomes...")

hh_income = persons.groupby("household_id")["income"].sum().reset_index()
hh_income.columns = ["household_id", "household_income"]

# remove existing column if script reruns
households = households.drop(columns=["household_income"], errors="ignore")

households = households.merge(hh_income, on="household_id")

print("Household incomes calculated.")


# ------------------------------------------------------------
# Car Ownership Model
# ------------------------------------------------------------
print("\nAssigning cars to households...")

cars = []

for i, (_, hh) in enumerate(households.iterrows()):

    income = hh["household_income"]
    size = hh["household_size"]

    # Base probability by income
    if income < 15000:
        p_car = 0.40
    elif income < 30000:
        p_car = 0.60
    elif income < 50000:
        p_car = 0.75
    elif income < 80000:
        p_car = 0.88
    else:
        p_car = 0.95

    # Household size effect (moderate)
    if size >= 3:
        p_car += 0.07
    if size >= 4:
        p_car += 0.10

    p_car = min(p_car, 0.95)

    # Assign cars
    if np.random.rand() > p_car:
        num_cars = 0
    else:

        if income > 70000 and size >= 3:

            r = np.random.rand()

            if r < 0.15:
                num_cars = 3
            elif r < 0.50:
                num_cars = 2
            else:
                num_cars = 1

        elif income > 50000 and size >= 2 and np.random.rand() < 0.30:
            num_cars = 2

        else:
            num_cars = 1

    cars.append(num_cars)

    if i % 1000 == 0:
        print(f"Processed {i} households...")

households["num_cars"] = cars

print("Car assignment completed.")


# ------------------------------------------------------------
# Assign Car Access to Individuals
# ------------------------------------------------------------
print("\nAssigning car access to persons...")

persons["car_access"] = 0

for i, (hh_id, group) in enumerate(persons.groupby("household_id")):

    n_cars = households.loc[
        households["household_id"] == hh_id, "num_cars"
    ].values[0]

    if n_cars == 0:
        continue

    # eligible drivers
    drivers = group[group["age"] >= 18]

    if len(drivers) == 0:
        continue

    # shared household access
    n_access = min(n_cars * 2, len(drivers))

    chosen = drivers.sample(n=n_access)

    persons.loc[chosen.index, "car_access"] = 1

    if i % 1000 == 0:
        print(f"Processed {i} households for car access...")

print("Car access assignment completed.")


# ------------------------------------------------------------
# Assign Bike Access
# ------------------------------------------------------------
print("\nAssigning bike access...")

persons["bike_access"] = 0

eligible = persons[persons["age"] >= 10]

target = int(len(persons) * 0.30)

print("Target bikes:", target)

chosen = eligible.sample(n=target)

persons.loc[chosen.index, "bike_access"] = 1

print("Bike assignment completed.")


# ------------------------------------------------------------
# Clean helper column
# ------------------------------------------------------------
persons = persons.drop(columns=["age"])


# ------------------------------------------------------------
# Save updated datasets
# ------------------------------------------------------------
print("\nSaving datasets...")

persons.to_csv(persons_file, index=False)
households.to_csv(households_file, index=False)


# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------
print("\n===================================")
print("Mobility Assignment Completed")
print("===================================")

print("Households:", len(households))
print("Persons:", len(persons))

print("\nCars distribution:")
print(households["num_cars"].value_counts())

print("\nHouseholds with cars (%):")
print(round((households["num_cars"] > 0).mean() * 100, 2))

print("\nBike access rate:")
print(round(persons["bike_access"].mean() * 100, 2), "%")

print("\nCar access rate:")
print(round(persons["car_access"].mean() * 100, 2), "%")

print("\nAverage household income:")
print(round(households["household_income"].mean(), 2))