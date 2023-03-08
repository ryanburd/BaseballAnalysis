# This code uses Pandas dataframes to analyze the correlation strength of standard defensive stats to advanced metric defensive stats. The goal is to determine which standard fielding stat(s) best correlates to the advanced metric outs above average (OAA), widely regarded as the best defensive metric for baseball players today.
#
# Standard stats (abbrev.): assists (A), assists from outfield (AOF), putouts (PO), errors (E), fielding percentage (FLD%), double plays (DP), games played (GP)
#
# All data is from 2022 Major League Baseball (MLB) games. OAA data is from Baseball Savant. Standard fielding data are from Fantrax. Only data from qualified fielders are used in correlation calculations, as defined by Baseball Savant. For 2B, SS, 3B, OF: 1 fielding attempt per team game played. For 1B: 1 fielding attempt per every other team game played. Catchers do not have OAA and so are not included here.

import pandas as pd
import matplotlib.pyplot as plt
from math import ceil
from unidecode import unidecode

def read_data(file_name):
    data = pd.read_csv(file_name)

    return data

def reformat_OAA_df(df, desired_stats):
    # For an OAA csv, remove the space in front of the first name and combine it with the last name as one new column. Change any accented letters to the closest unaccented letter. Rename columns for easier reading.
    df['Player'] = df[' first_name'].map(lambda x: unidecode(x.lstrip(' '))) + " " + df['last_name'].map(lambda x: unidecode(x))
    df = df.rename(columns={'primary_pos_formatted' : 'Pos'})
    df = df.rename(columns={'outs_above_average' : 'OAA'})

    # Select only the desired stats from the dataframe.
    df = df[desired_stats].copy()

    return df

def reformat_std_df(df, desired_stats):
    # For the standard fielding csv, only include players with at least 1 game played (this removes prospects not in the MLB who may have the same name as an MLB player). Remove the quotes around the player name. Remove the thousands separator from all stats and recast to int.
    df = df[df['GP'] > 0]
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

class PositionGroup:

    # Create a list of all positions contained within the group. Select only those positions from the all positions dataframe.
    def __init__(self, positions, allPos_df):
        self.positions = positions
        self.df = allPos_df[allPos_df['Pos'].isin(self.positions)]

        # If no outfield positions are included, remove AOF (outfield only stat).
        if not any(position in self.positions for position in ['LF', 'CF', 'RF']):
            self.df = self.df.drop(columns=['AOF'])
    
    def calculate_corr(self):
        self.corr_matrix = self.df.corr()
    
    def plot_corr_coeff(self, corr_stat, ax):
        # Remove the stat to which all others should be correlated (corr_stat). It's going to have a correlation coefficient of 1 with itself.
        self.corr_matrix = self.corr_matrix.drop(corr_stat)

        # Plot the other stats' correlation coefficient with corr_stat.
        self.corr_matrix[[corr_stat]].plot(ax=ax, kind='bar')
        ax.set_title(', '.join(self.positions))
        ax.set_xlabel('Defensive stat')
        ax.set_ylabel('Correlation coefficient w/ %s' % corr_stat)

def plot_position_groups(groups, df):
    num_groups = len(groups)
    num_rows = 2
    num_cols = ceil(num_groups/num_rows)
    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, sharey=True)

    group_index = 0
    for row in range(num_rows):
        for col in range(num_cols):
            if group_index < num_groups:
                # Create a dataframe containing only the positions within the group
                PG = PositionGroup(groups[group_index], df)
                group_index += 1

                # Calculate correlation matrix of the dataframe.
                PG.calculate_corr()

                # Create a bar graph of the correlation coefficients for each stat with the desired stat, corr_stat.
                corr_stat = 'OAA'
                PG.plot_corr_coeff(corr_stat, axes[row, col])
    
    plt.tight_layout()
    plt.show()

def main():

    # Read in defensive stats from csv files.
    folder = 'FieldingStats/'
    OAA_df = read_data(folder+'outs_above_average.csv')
    std_df = read_data(folder+'standard_fielding.csv')

    # Reformat the player name column in each dataframes so they can be properly merged by player name. Then keep only the desired stats in the dataframe.
    desired_OAA_stats = ['Player', 'Pos', 'OAA']
    OAA_df = reformat_OAA_df(OAA_df, desired_OAA_stats)

    desired_std_stats = ['Player', 'A', 'AOF', 'PO', 'E', 'FLD%', 'DP', 'GP']
    std_df = reformat_std_df(std_df, desired_std_stats)

    # Merge the OAA and standard stats into one dataframe. Sort the merged dataframe by the desired stat.
    sort_stat = 'OAA'
    merged_df = merge_OAA_std(OAA_df, std_df, sort_stat)

    # Create a figure showing the correlation coefficients between OAA and standard defensive stats for different position groups.
    all_positions = ['1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF']
    infield = ['1B', '2B', '3B', 'SS']
    infield_no1B = ['2B', '3B', 'SS']
    outfield = ['LF', 'CF', 'RF']
    groups = [infield, infield_no1B, outfield, all_positions]
    plot_position_groups(groups, merged_df)

    # Create a figure of the correlation coefficients for each position individually.
    individual_positions = [['1B'], ['2B'], ['3B'], ['SS'], ['LF'], ['CF'], ['RF']]
    plot_position_groups(individual_positions, merged_df)

if __name__ == "__main__":
    main()