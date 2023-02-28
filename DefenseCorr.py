# This code uses Pandas dataframes to analyze the correlation strength of standard defensive stats to advanced metric defensive stats. The goal is to determine which standard fielding stat(s) best correlates to the advanced metric outs above average (OAA), widely regarded as the best defensive metric for baseball players today.
#
# Standard stats (abbrev.): assists (A), assists from outfield (AOF), putouts (PO), errors (E), fielding percentage (FLD%), double plays (DP), caught stealing against (CSA), stolen bases allowed (SBA), games played (GP)
#
# All data is from 2022 Major League Baseball (MLB) games. OAA data is from Baseball Savant. Standard fielding data are from Fantrax. Only qualified fielders (defined by Baseball Savant as having played 1 inning in the field per team game played) are used in correlation calculations.

import pandas as pd
import matplotlib.pyplot as plt

def read_data(file_name):
    data = pd.read_csv(file_name)

    return data

def reformat_OAA_df(df, desired_stats):
    # For an OAA csv, remove the space in front of the first name and combine it with the last name as one new column. Rename columns for easier reading.
    df['Player'] = df[' first_name'].map(lambda x: x.lstrip(' ')) + " " + df['last_name']
    df = df.rename(columns={'primary_pos_formatted' : 'Pos'})
    df = df.rename(columns={'outs_above_average' : 'OAA'})

    # Select only the desired stats from the dataframe.
    df = df[desired_stats].copy()

    return df

def reformat_std_df(df, desired_stats):
    # For the standard fielding csv, remove the quotes around the player name. Remove the thousands separator from PO and recast to int.
    df['Player'] = df['Player'].map(lambda x: x.lstrip('"').rstrip('"'))
    df = df.replace(',','', regex=True)
    df['PO'] = df['PO'].astype(int)

    # Select only the desired stats from the dataframe.
    df = df[desired_stats].copy()

    return df

def merge_OAA_std(OAA_df, std_df, sort_stat):
    merged_df = OAA_df.merge(std_df, how='inner', on='Player')
    merged_df = merged_df.sort_values(by=[sort_stat], ascending=False)

    return merged_df

class PositionDf:

    # Create a list of all positions contained within the group. Select only those positions from the all positions dataframe.
    def __init__(self, positions, allPos_df):
        self.positions = positions
        self.df = allPos_df[allPos_df['Pos'].isin(self.positions)]

        # If no outfield positions are included, remove AOF (outfield only stat).
        if any(position in self.positions for position in ['LF', 'CF', 'RF']):
            self.df = self.df.drop(columns=['AOF'])

        # If catchers are not included, remove CSA and SBA (catcher only stats).
        if 'C' not in self.positions:
            self.df = self.df.drop(columns=['CSA', 'SBA'])
    
    def calculate_corr(self):
        self.corr_matrix = self.df.corr()
    
    def plot_corr_coeff(self, corr_stat):
        # Remove the stat to which all others should be correlated (corr_stat). It's going to have a correlation coefficient of 1 with itself.
        self.corr_matrix = self.corr_matrix.drop(corr_stat)

        # Plot the other stats' correlation coefficient with corr_stat.
        fig, ax = plt.subplots(nrows=1, ncols=1)
        self.corr_matrix[[corr_stat]].plot(ax=ax, kind='bar')
        ax.set_title(', '.join(self.positions))
        ax.set_xlabel('Defensive stat')
        ax.set_ylabel('Correlation coefficient w/ %s' % corr_stat)
        plt.show()

# def plot_corr_coeff(corr_matrix, corr_stat):

#     fig1, axes = plt.subplots(nrows=1, ncols=3, sharey=True)

#     corr_matrix = corr_matrix.drop(corr_stat)
#     corr_matrix[[corr_stat]].plot(ax=axes[0], kind='bar')
#     axes[0].set_title('All positions')
#     # axes[0].set_xlabel('Standard defensive stat')
#     axes[0].set_ylabel('Correlation coefficient')

def main():

    # Read in defensive stats from csv files.
    OAA_df = read_data('outs_above_average.csv')
    std_df = read_data('standard_fielding.csv')

    # Reformat the player name column in each dataframes so they can be properly merged by player name. Then keep only the desired stats in the dataframe.
    desired_OAA_stats = ['Player', 'Pos', 'OAA']
    OAA_df = reformat_OAA_df(OAA_df, desired_OAA_stats)

    desired_std_stats = ['Player', 'A', 'AOF', 'PO', 'E', 'FLD%', 'DP', 'CSA', 'SBA', 'GP']
    std_df = reformat_std_df(std_df, desired_std_stats)

    # Merge the OAA and standard stats into one dataframe. Sort the merged dataframe by the desired stat.
    sort_stat = 'OAA'
    merged_df = merge_OAA_std(OAA_df, std_df, sort_stat)

    # Create a position grouping for correlation calculations. Create a dataframe containing only those positions.
    positions = ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF']
    all_positions = PositionDf(positions, merged_df)

    # Calculate correlation matrix of the merged dataframe.
    all_positions.calculate_corr()

    # Create a bar graph of the correlation coefficients for each stat with the desired stat, corr_stat.
    corr_stat = 'OAA'
    all_positions.plot_corr_coeff(corr_stat)

if __name__ == "__main__":
    main()

# def by_position():
#     ncols = 4
#     fig2, axes = plt.subplots(nrows=2, ncols=ncols, sharey=True)
#     pos = ['1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'C']

#     for i in range(len(pos)):
#         pos_stats = merged_stats[merged_stats['Pos'].isin([pos[i]])]
#         if pos[i] in infield:
#             pos_stats = pos_stats.drop(columns=['AOF', 'CSA', 'SBA'])
#         elif pos[i] in outfield:
#             pos_stats = pos_stats.drop(columns=['A', 'DP', 'CSA', 'SBA'])
#         pos_corr = pos_stats.corr()
#         pos_corr = pos_corr.drop('OAA')
#         if i < ncols:
#             pos_corr[['OAA']].plot(ax=axes[0,i], kind='bar')
#             axes[0,i].set_title(pos[i])
#         else:
#             pos_corr[['OAA']].plot(ax=axes[1,i-ncols], kind='bar')
#             axes[1,i-ncols].set_title(pos[i])

    
#     plt.show()

# by_position()