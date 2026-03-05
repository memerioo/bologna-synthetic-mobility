# TPB Mobility Bologna

Synthetic population + TPB-based mobility simulation for Bologna (aree statistiche).

This Project is devided in the following steps:

1. Gathering Data and general exploration

2. Processing Data according to the goals (merging, aggregation, disaggregation, proxy, etc.)
We add .json file for constraints, like total university students, total cars, and target population. 

We disaggregate households dataset, which exists in zones, into area level, becasue other data exists in area level, and targeted spatial unit is statistical areas. We wil ldo so accordin to population share of each area in its zone.

In this process we will have altered data due to some logics, like mentioned disaggregation of households; or assigning numeric values to households size (random for 6-10 and randome between 11 and 15 for oltre 10)


3. Synthetic Population Generation

4. Mobility generation for Bologna, based on Theory of Planned Behaviour (TPB)

5. Evaluation

## 1. Data

Raw datasets are not included in this repository. They must be downloaded from their original sources (see docs/data_sources.md) and are subject to their respective licenses.

For most datasets a script is available via download data script, which is also included in the makefile.

The following dataset must be downloaded manually:
1. Go to:
https://public.tableau.com/app/profile/ufficio.statistiche.territoriali.bologna/viz/Dati_Mobilita_Comune_Bologna2023/Volumispostamenti
2. Click Download → Crosstab → CSV
3. Save as data/raw/occupation/graf poli.csv

##2. Processing Data

##3. Synthetic Population Generation

For synthetic population generation, we do household first. The logic is to prevent impossible combinations for households, eg infant living alone. Also some mobility constraints make sense in households level, for example car ownership, as people might share usage of a car even if they don't own it. 

We have a minimum variable profile, MVP, for both households and individuals: 
Househlods MVP:
household_id
zona
household_size
household_type
household_income
n_cars

individual MVP:
agent_id
household_id
age_group
sex
citizenship
employment_status
car_access
work_area
school_area

The algorithm for synthetic population generation would be a hybrid approach. For households we use combinnatorial/ constraint based. Then for individuals we will follow IPF algorithm with heuristic seed.

Then we will assign individuals to households, and the last step would be assign work/school locations.

##4. Mobility generation with TPB

##5. Evaluation
