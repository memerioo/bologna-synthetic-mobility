# TPB Mobility Bologna

Synthetic population + TPB-based mobility simulation for Bologna (aree statistiche).

This Project is devided in the following steps:

1. Gathering Data and general exploration

2. Processing Data according to the goals (mergin, aggregation, disaggregation, proxy, etc.)

3. Synthetic Population Generation

4. Mobility generation for Bologna, based on Theory of Planned Behaviour (TPB)

5. Evaluation

Data

Raw datasets are not included in this repository. They must be downloaded from their original sources (see docs/data_sources.md) and are subject to their respective licenses.

For most datasets a script is available via download data script, which is also included in the makefile.

The following dataset must be downloaded manually:
1. Go to:
https://public.tableau.com/app/profile/ufficio.statistiche.territoriali.bologna/viz/Dati_Mobilita_Comune_Bologna2023/Volumispostamenti
2. Click Download → Crosstab → CSV
3. Save as data/raw/occupation/graf poli.csv


