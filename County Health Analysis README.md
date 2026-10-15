# County Health Disparities: Race, Rurality, and Overdoses

An analysis of 2025 County Health Rankings data for 3,000+ U.S. counties using Python (pandas), SQL, and R.

## Questions

1. How large is the gap between Black and White children in poverty, and between Black and White median household income?
2. Do mostly rural counties have higher uninsured rates, fewer primary care physicians, and more preventable hospital stays than mostly urban counties?
3. How does West Virginia's drug overdose death rate compare with the rest of the U.S.?

## Data

Source: County Health Rankings & Roadmaps, University of Wisconsin Population Health Institute (2025 analytic dataset), countyhealthrankings.org

The raw file has 796 columns. This project keeps 16 of them. The raw CSV is not included; the cleaned file (County_Health.csv) is.

## Approach

- Python (pandas): cleaning the data and creating charts
- SQL: exploring and summarizing the data
- R: statistical tests

## Key Findings

- Median child poverty is 33.6% for Black children vs. 11.8% for White children, across 1,630 counties. Median household income differs by about $25,000.
- Mostly rural counties have about half as many primary care physicians per person as mostly urban counties (38 vs. 79 per 100,000). Preventable hospital stays barely differ.
- West Virginia's overdose death rate is 78.0 per 100,000, the highest of any state and 2.6 times the rest of the U.S. (30.6).

## Limitations

- Findings describe counties, not individuals.
- Many small counties are missing data, especially for race-specific measures and overdose deaths.
- These results show associations, not causes.
