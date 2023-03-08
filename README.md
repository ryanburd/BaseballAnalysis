# BaseballAnalysis
This repository contains Python code that calculates correlations between various baseball statistics using data collected from Major League Baseball games. Data sources include Baseball Savant, Baseball-Reference, and Fantrax. Pandas software library is used for all data analysis.

## Python scripts
- DefenseCorr.py: calculates correlations between standard defensive stats and Baseball Savant's outs above average (OAA)
- StatsByYear.py: plots the yearly league averages of many stats (batting, fielding, pitching, misc) by year

## Stat folders
### FieldingStats
- outs_above_average.csv: contains the outs above average (OAA) from Baseball Savant for all qualified fielders from the 2022 MLB season.
- standard_fielding.csv: contains several common fielding stats recorded by Fantrax for all fielders from the 2022 MLB season.

### YearlyStats
- batting_yearly_averages.csv: contains the per game averages by year for several batting statistics recorded by Baseball-Reference for each MLB season from 1871-2022
- fielding_yearly_averages.csv: contains the per game averages by year for several fielding statistics recorded by Baseball-Reference for each MLB season from 1871-2022
- pitching_yearly_averages.csv: contains the per game averages by year for several pitching statistics recorded by Baseball-Reference for each MLB season from 1871-2022
- misc_yearly_averages.csv: contains the per game averages by year for several general statistics recorded by Baseball-Reference for each MLB season from 1876-2022