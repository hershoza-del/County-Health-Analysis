An analysis of 2025 County Health Rankings data for U.S. counties, using Python (Pandas), Excel, SQL, and R. 

Questions

1. How do black and white people differ in terms of child poverty rates and median household income?
2. To what extent does living in a mostly rural or mostly urban have an impact on uninsured rates, primary care physician rates, and preventable hospital stays? 
3. How does West Virginia's drug overdose rate compare with other states?

Approach

Python (Pandas): cleaning/rearranging the dataset and creating charts based on the questions I asked
Excel: cross-checking the dataset with vlookups, xlookups, if(s) functions and creating a pivottable
SQL: querying the questions I asked
R: running statistical tests regarding the questions I asked

Key Findings

Median child poverty is 33.6% for Black children vs. 11.8% for White children, across 1,630 counties. Median household income differs by about $25,000.
Mostly rural counties have about half as many primary care physicians per person as mostly urban counties (38 vs. 79 per 100,000). Preventable hospital stays barely differ.
West Virginia's overdose death rate is 78.0 per 100,000, the highest of any state and 2.6 times the rest of the U.S. (30.6).

Limitations

Findings describe counties, not individuals.
Many small counties are missing data, especially for race-specific measures and overdose deaths.
These results show associations, not causes.

Data

Source: County Health Rankings & Roadmaps, University of Wisconsin Population Health Institute (2025 analytic dataset), countyhealthrankings.org

The raw file has 796 columns. This project keeps 16 of them. The raw CSV is not included; the cleaned file (County_Health_Analysis.csv) is.
