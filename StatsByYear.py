# This code shows the change in league average baseball stats per year. Data were obtained from Baseball-Reference.
#
# Batting stats used:
#
# Fielding stats used:
#
# Pitching stats used:
#
# Fielding stats used:
#
# Notable changes comparing 1900-1920 to 2022 (try averaging multiple seasons for comparison with recent history to account for yearly changes in the ball):
# - SH decreased            -> SH (hitting)??? -> NO; this seems to correlate with PH/G, which would be bad for fantasy lineups
# - 3B decreased            -> 3B (hitting)???
# - 1B decreased*           -> BA (hitting) or something else that emphasizes putting the ball in play more
# - SB decreased            -> SB (hitting)
# - CS decreased
# - CS% decreased
# - SO increased            -> SO (hitting)
# - HR increased            -> HR or HR/9 (pitching)
# - 2B, TB increased*       -> TB (pitching)???
# - BB increased*           -> BB or BB/9 (pitching)???
# - E decreased
# - A decreased
# - DP increased
# - R increased*            -> R (hitting) (they weren't trying to hit for power, but they were trying to score runs)
# - ER increased            -> ER or ERA (pitching)
# - ER/R increased
# - Pitchers/G increased    -> IP (pitching)
# - PR/G increased

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read in data. Change the index to Year.
batting_stats_all = pd.read_csv('batting_yearly_averages.csv')
batting_stats_all = batting_stats_all.set_index('Year')
fielding_stats_all = pd.read_csv('fielding_yearly_averages.csv')
fielding_stats_all = fielding_stats_all.set_index('Year')
pitching_stats_all = pd.read_csv('pitching_yearly_averages.csv')
pitching_stats_all = pitching_stats_all.set_index('Year')
misc_stats_all = pd.read_csv('misc_yearly_averages.csv')
misc_stats_all = misc_stats_all.set_index('Year')

# Select desired stats. Remove years with NaN. Recast stats to type float. For CS% under fielding stats, remove the % symbol for conversion to float.
batting_stats = batting_stats_all[['R', 'H', '1B', '2B', '3B', 'HR', 'RBI', 'TB', 'BB', 'SO', 'SH', 'SB', 'BA', 'OBP', 'SLG', 'OPS']].copy().dropna().astype(float)

pitching_stats = pitching_stats_all[['R', 'ER', 'H', 'HR', 'BB', 'SO', 'ERA', 'WHIP', 'BAbip']].copy().dropna().astype(float)
pitching_stats['ER/R'] = pitching_stats['ER'] / pitching_stats['R']

fielding_stats_all['CS%'] = fielding_stats_all['CS%'].astype(str).map(lambda x: x.rstrip('%'))
fielding_stats = fielding_stats_all[['Ch', 'A', 'PO', 'E', 'DP', 'Fld%', 'SB', 'CS', 'CS%']].copy().dropna().astype(float)

misc_stats = misc_stats_all[['R/G', 'PA/G', 'Batters/G', 'Pitchers/G', 'PH/G', 'PR/G']].copy().dropna().astype(float)

# Normalize each stat to the 2022 value.
batting_stats_norm = (batting_stats - batting_stats.values[0,:]) / batting_stats.values[0,:]
fielding_stats_norm = (fielding_stats - fielding_stats.values[0,:]) / fielding_stats.values[0,:]
pitching_stats_norm = (pitching_stats - pitching_stats.values[0,:]) / pitching_stats.values[0,:]
misc_stats_norm = (misc_stats - misc_stats.values[0,:]) / misc_stats.values[0,:]

# Plot normalized stats by year.
fig, axes = plt.subplots(nrows=2, ncols=2, sharex = True, sharey=True)

colormap = plt.cm.nipy_spectral
colors = colormap(np.linspace(0, 1, 16))
axes[0,0].set_prop_cycle('color', colors)
batting_stats_norm.plot.line(ax=axes[0,0])
axes[0,0].set_title('Batting')
axes[0,0].legend(loc='upper center', ncols=8, fontsize=8)

fielding_stats_norm.plot.line(ax=axes[0,1])
axes[0,1].set_title('Fielding')
axes[0,1].legend(loc='upper right', ncols=5, fontsize=8)

pitching_stats_norm.plot.line(ax=axes[1,0])
axes[1,0].set_title('Pitching')
axes[1,0].legend(loc='upper right', ncols=5, fontsize=8)

misc_stats_norm.plot.line(ax=axes[1,1])
axes[1,1].set_title('Misc')
axes[1,1].legend(loc='upper right', ncols=3, fontsize=8)

plt.xlim([1900, 2022])
plt.ylim([-1, 2])

plt.show()

print(misc_stats.head())