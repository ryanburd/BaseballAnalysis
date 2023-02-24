# This code analyses the correlation strength of standard defensive stats to advanced metric defensive stats. The goal is to determine which standard fielding stat(s) best correlates to the advanced metric outs above average (OAA), widely regarded as the best defensive metric for baseball players today.

import pandas as pd

# Read defensive stats data from csv files.
OAA_2022_all = pd.read_csv('outs_above_average.csv')
StdField_2022_all = pd.read_csv('standard_fielding.csv')

# Create new dataframes with only the desired stats.
# 
# First, reformat the player name columns as necessary so they can be properly merged:
# For OAA csv, remove the space in front of the first name and combine it with the last name as one new column. Rename 'outs_above_average' to 'OAA'.
OAA_2022_all['Player'] = OAA_2022_all[' first_name'].map(lambda x: x.lstrip(' ')) + " " + OAA_2022_all['last_name']
OAA_2022_all = OAA_2022_all.rename(columns={'outs_above_average' : 'OAA'})

OAA_2022 = OAA_2022_all[['Player', 'OAA']].copy()

# For the standard fielding csv, remove the quotes around the player name.
StdField_2022_all['Player'] = StdField_2022_all['Player'].map(lambda x: x.lstrip('"').rstrip('"'))

StdField_2022 = StdField_2022_all[['Player', 'A', 'AOF', 'PO', 'E', 'FLD%', 'DP', 'CSA', 'SBA', 'GP']].copy()

# Merge the dataframes.
merged_stats = OAA_2022.merge(StdField_2022, how='inner', on='Player')
merged_stats = merged_stats.sort_values(by=['OAA'], ascending=False)

print(merged_stats)