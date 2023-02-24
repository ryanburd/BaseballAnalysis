# This code analyses the correlation strength of standard defensive stats to advanced metric defensive stats. The goal is to determine which standard fielding stat(s) best correlates to the advanced metric outs above average (OAA), widely regarded as the best defensive metric for baseball players today.
#
# Standard stats (abbrev.): assists (A), assists from outfield (AOF), putouts (PO), errors (E), fielding percentage (FLD%), double plays (DP), caught stealing against (CSA), stolen bases allowed (SBA), games played (GP)
#
# All data is from 2022 Major League Baseball (MLB) games. OAA data is from Baseball Savant. Standard fielding data are from Fantrax. Only qualified fielders (defined by Baseball Savant as having played 1 inning in the field per team game played) are used in correlation calculations.

import pandas as pd
import matplotlib.pyplot as plt

# Read defensive stats data from csv files.
OAA_2022_all = pd.read_csv('outs_above_average.csv')
StdField_2022_all = pd.read_csv('standard_fielding.csv')

# Create new dataframes with only the desired stats.
# 
# First, reformat the player name columns as necessary so they can be properly merged:
# For OAA csv, remove the space in front of the first name and combine it with the last name as one new column. Rename columns for easier reading.
OAA_2022_all['Player'] = OAA_2022_all[' first_name'].map(lambda x: x.lstrip(' ')) + " " + OAA_2022_all['last_name']
OAA_2022_all = OAA_2022_all.rename(columns={'primary_pos_formatted' : 'Pos'})
OAA_2022_all = OAA_2022_all.rename(columns={'outs_above_average' : 'OAA'})

OAA_2022 = OAA_2022_all[['Player', 'Pos', 'OAA']].copy()

# For the standard fielding csv, remove the quotes around the player name. Remove the thousands separator from PO and recast to int.
StdField_2022_all['Player'] = StdField_2022_all['Player'].map(lambda x: x.lstrip('"').rstrip('"'))
StdField_2022_all = StdField_2022_all.replace(',','', regex=True)
StdField_2022_all['PO'] = StdField_2022_all['PO'].astype(int)
StdField_2022_all['FP+A'] = StdField_2022_all['FLD%'] + StdField_2022_all['A']

StdField_2022 = StdField_2022_all[['Player', 'A', 'AOF', 'PO', 'E', 'FLD%', 'DP', 'FP+A', 'CSA', 'SBA', 'GP']].copy()

# Merge the dataframes.
merged_stats = OAA_2022.merge(StdField_2022, how='inner', on='Player')
merged_stats = merged_stats.sort_values(by=['OAA'], ascending=False)

# Calculate and show bar graph of correlations between OAA and standard defensive stats. Use all defensive positions for correlations.
fig1, axes = plt.subplots(nrows=1, ncols=3, sharey=True)

allPOS_corr = merged_stats.corr()
allPOS_corr = allPOS_corr.drop('OAA')
allPOS_corr[['OAA']].plot(ax=axes[0], kind='bar')
axes[0].set_title('All positions')
# axes[0].set_xlabel('Standard defensive stat')
axes[0].set_ylabel('Correlation coefficient')

# Calculate and show bar graph of correlations between OAA and standard defensive stats. Use only infield positions (1B, 2B, 3B, SS) for correlations. Remove N/A stats for infielders.
infield = ['1B', '2B', '3B', 'SS']
IF_stats = merged_stats[merged_stats['Pos'].isin(infield)]
IF_stats = IF_stats.drop(columns=['AOF', 'CSA', 'SBA'])
IF_corr = IF_stats.corr()
IF_corr = IF_corr.drop('OAA')
IF_corr[['OAA']].plot(ax=axes[1], kind='bar')
axes[1].set_title('Infield positions')
axes[1].set_xlabel('Standard defensive stat')
# axes[1].set_ylabel('Correlation coefficient')

# Calculate and show bar graph of correlations between OAA and standard defensive stats. Use only outfield positions (LF, CF, RF) for correlations. Remove N/A stats for outfielders.
outfield = ['LF', 'CF', 'RF']
OF_stats = merged_stats[merged_stats['Pos'].isin(outfield)]
OF_stats = OF_stats.drop(columns=['CSA', 'SBA'])
OF_corr = OF_stats.corr()
OF_corr = OF_corr.drop('OAA')
OF_corr[['OAA']].plot(ax=axes[2], kind='bar')
axes[2].set_title('Outfield positions')
# axes[2].set_xlabel('Standard defensive stat')
# axes[2].set_ylabel('Correlation coefficient')

plt.show()

def by_position():
    ncols = 4
    fig2, axes = plt.subplots(nrows=2, ncols=ncols, sharey=True)
    pos = ['1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'C']

    for i in range(len(pos)):
        pos_stats = merged_stats[merged_stats['Pos'].isin([pos[i]])]
        if pos[i] in infield:
            pos_stats = pos_stats.drop(columns=['AOF', 'CSA', 'SBA'])
        elif pos[i] in outfield:
            pos_stats = pos_stats.drop(columns=['A', 'DP', 'CSA', 'SBA'])
        pos_corr = pos_stats.corr()
        pos_corr = pos_corr.drop('OAA')
        if i < ncols:
            pos_corr[['OAA']].plot(ax=axes[0,i], kind='bar')
            axes[0,i].set_title(pos[i])
        else:
            pos_corr[['OAA']].plot(ax=axes[1,i-ncols], kind='bar')
            axes[1,i-ncols].set_title(pos[i])

    
    plt.show()

by_position()