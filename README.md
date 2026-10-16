# County Health Analysis

An analysis of 2025 County Health Rankings data for 3,000+ U.S. counties.

## Approach

- Python (pandas and matplotlib): cleaning the data and creating charts for each question (charts can be found on my Hersh Oza LinkedIn page) 
- SQL: exploring and summarizing the data for each question
- R: running statistical tests for each question

## Questions

1. How large is the gap between Black and White children in poverty, and between Black and White median household income?
2. Do mostly rural counties have higher uninsured rates, fewer primary care physicians, and more preventable hospital stays than mostly urban counties?
3. How does West Virginia's drug overdose death rate compare with the rest of the U.S.?

## Question 1 (Race)

- Across the 1,630 counties that report both groups, median child poverty is 33.6% for Black children vs. 11.8% for White children. On average, the Black rate is 21.7 percentage points higher in the same county.
- Across 1,767 counties, Black median household income is $44,892 vs. $69,841 for White median households. On average, Black households earn $21,874 less in the same county.

## Question 2 (Rural)

- Mostly rural counties have about 37% fewer primary care physicians: an average of around 44 vs. 70 per 100,000. This gap remains after controlling for income.
- Mostly rural counties hoist a uninsured rate, but only by a little: 11.0% vs. 9.6% on average. About two-thirds of this gap is explained by income; rural counties tend to be poorer.
- Mostly rural counties have slightly more preventable hospital stays: 2,905 vs. 2,693 per 100,000 people on average. However, this difference is driven by income. Comparing counties with the same median income, more rural counties have slightly fewer preventable stays.

## Question 3 (West Virginia)

- West Virginia's statewide overdose death rate is 78.0 per 100,000, the highest of any state.
- At the county level, West Virginia counties average 76.1 deaths per 100,000 vs. 31.8 for all other counties, about 2.4 times higher.

## Limitations

- Findings describe counties, not individuals.
- County averages weight every county equally regardless of population, so they differ slightly from statewide rates.
- Many small counties are missing data, especially for race-specific measures and overdose deaths. Overdose rates are suppressed for 1,142 counties (36%), including 10 of West Virginia's 55 counties, so the county-level overdose comparison mostly reflects larger counties.
- The race comparisons include only counties that report data for both groups, which leaves out many counties with small Black populations.
- These results show associations, not causes.
- Population was based from 2020-2022 data. 
- MOST IMPORTANTLY: these results are solely based from this dataset

## Data Source

County Health Rankings & Roadmaps, University of Wisconsin Population Health Institute (2025 analytic dataset), countyhealthrankings.org
