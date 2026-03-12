# TPB Mobility Bologna

Synthetic population + TPB-based mobility simulation for Bologna (aree statistiche).

This Project is devided in the following steps:

1. Gathering Data and general exploration

2. Processing Data according to the goals

3. Synthetic Population Generation

4. Mobility generation for Bologna, based on Theory of Planned Behaviour (TPB)

5. Evaluation

## 1. Data

Raw datasets are not included in this repository. They must be downloaded from their original sources (see data/README.md) and are subject to their respective licenses.

For most datasets a script is available via download data script, which is also included in the makefile.

The following dataset must be downloaded manually:
1. Go to:
https://public.tableau.com/app/profile/ufficio.statistiche.territoriali.bologna/viz/Dati_Mobilita_Comune_Bologna2023/Volumispostamenti
2. Click Download → Crosstab → CSV
3. Save as data/raw/occupation/graf poli.csv

## 2. Processing Data

We disaggregate households dataset, which exists in zones, into area level, becasue other data exists in area level, and targeted spatial unit is statistical areas. We wil ldo so accordin to population share of each area in its zone.

In this process we will have altered data due to some logics, like mentioned disaggregation of households; or assigning numeric values to households size (random for 6-10 and randome between 11 and 15 for oltre 10)

## 3. Synthetic Population Generation

The synthetic population for Bologna is generated through a multi-stage process, beginning with household creation and followed by individual generation and assignment.

The design prioritizes logical consistency and realistic demographic distributions, ensuring that impossible household configurations (e.g., infants living alone) cannot occur. Additionally, certain mobility attributes, such as vehicle ownership, are naturally modeled at the household level, since cars are typically shared resources among household members.


### 3.1 Minimum Variable Profiles

To keep the synthetic population compact while still supporting mobility simulation, a **Minimum Variable Profile (MVP)** is defined for both households and individuals.

#### Household MVP

| Variable | Description |
|--------|-------------|
| household_id | unique household identifier |
| area_name | statistical area of residence |
| household_size_cat | size of the household catagorial |
| household_size | household size numerical |
| household_income | aggregated household income |
| num_cars | number of vehicles owned |

#### Individual MVP

| Variable | Description |
|--------|-------------|
| person_id | unique individual identifier |
| household_id | household membership |
| age_group | age category |
| sex | gender |
| citizenship | nationality category |
| employment_status | worker / student / inactive |
| car_access | access to a household car |
| bike_access | access to individual bike |
| work_area | workplace statistical area |
| school_area | school location |


### 3.2 Household Generation

Households are generated first using a constraint-based combinatorial approach informed by observed demographic statistics.

The generation process follows these steps:

1. Household sizes are sampled from the empirical household size distribution.
2. Households are spatially allocated according to population statistics for Bologna’s statistical areas.
3. Logical constraints ensure that unrealistic household configurations cannot occur.

This step establishes the structural framework into which individuals will later be placed.


### 3.3 Individual Generation

Individuals are then generated and assigned to households.

Rather than using full iterative proportional fitting (IPF), individuals are produced through probabilistic sampling from demographic distributions, including:

- age group distributions
- sex ratios
- employment and student status
- citizenship categories
- income distributions

Sampling probabilities are calibrated to match aggregate statistics for Bologna.

Generated individuals are then assigned to households while respecting household size and composition constraints.


### 3.4 Mobility Attributes

After the core population is generated, additional attributes relevant to mobility modeling are assigned.

#### Household Level
- household income (aggregated from individuals)
- number of cars

Vehicle ownership is probabilistically assigned based on household income and household size, approximating observed car ownership rates in Bologna.

#### Individual Level
- car access
- bicycle access

Car access depends on both household vehicle ownership and driver eligibility, while bicycle access is assigned probabilistically to reflect Bologna’s relatively high cycling prevalence.


### 3.5 Activity Locations

In the final step, activity locations are assigned:

- workers receive workplace areas
- students receive school areas

These locations are sampled from the observed origin–destination activity distributions across Bologna’s statistical zones.


### 3.6 Result

The resulting synthetic population reproduces key aggregate statistics of Bologna, including:

- population totals
- age structure
- household composition
- employment and student distributions
- vehicle ownership patterns

This population can then be used as the basis for agent-based mobility simulations.


## 4. Mobility generation with TPB

## 5. Evaluation
