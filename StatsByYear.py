# This code shows the change in MLB league average stats per year. Data were obtained from Baseball-Reference.
#
# All stats are already provided as per game averages, allowing for comparison of how the league averages for each stat changed over the years regardless of how many games were played each season.
#
# The stats are plotted by year as percent changes relative to the average over a reference year range controlled by the user. This normalization allows for comparison of how drastically each stat has changed over the years, providing inside for how baseball strategy has developed.
# 
# Currently, the 1908-1919 year range is used as the reference to show how stats have changed relative to the "dead-ball era," a time when runs/game were at some of their lowest in history and offensive strategies favored contact hitting over power hitting. 1908 is the earliest year for some of the recorded stats used here, and 1919 marked the last year before many batters across the league started copying Babe Ruth's new power hitting strategy. 

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class statGroup:

    def __init__(self, group_name, file_name, stats):
        self.group_name = group_name
        self.file_name = file_name
        self.stats = stats
    
    def prepare_dataframe(self, index):
        self.df = pd.read_csv(self.file_name)
        self.df = self.df.set_index(index)

        # Select desired stats. Remove years with NaN. Recast stats to type float. For CS% under fielding stats, remove the % symbol for conversion to float.
        if 'CS%' in self.df.columns:
            self.df['CS%'] = self.df['CS%'].astype(str).map(lambda x: x.rstrip('%'))
        self.df = self.df[self.stats].copy().dropna().astype(float)
    
    def calculate_percent_change(self, ref_year_start, ref_year_end):
        # Calculate the average of each stat over the given year range.
        ref_averages = self.df.loc[ref_year_start,:]
        for year in range(ref_year_start + 1, ref_year_end + 1):
            ref_averages += self.df.loc[year,:]
        ref_averages /= (ref_year_end - ref_year_start + 1)

        # Calculate the percent change of each stat each year relative to the reference averages.
        self.df = (self.df - ref_averages) / ref_averages
    
    def plot_by_year(self, ax, ref_year_start, ref_year_end):
        # Set colormap.
        colormap = plt.cm.nipy_spectral
        colors = colormap(np.linspace(0, 1, len(self.stats)))
        ax.set_prop_cycle('color', colors)

        # Plot the stats and a horizontal line for the reference average.
        self.df.plot.line(ax=ax)
        ax.axhline(y=0, color='black', linestyle='dashed')

        # Plot design
        ax.set_title(self.group_name)
        ax.set_xlabel('Year')
        ax.set_ylabel('Percent change relative to %i-%i'%(ref_year_start, ref_year_end))
        ax.legend(ncols=4, fontsize=8)

def plot_stats_by_year(groups, ref_year_start, ref_year_end):
    nrows = 2
    ncols = 2
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, sharey=True)

    start_year = 1900
    end_year = 2022
    plt.xlim([start_year, end_year])

    max_decrease = -1
    max_increase = 2
    plt.ylim([max_decrease, max_increase])

    group_index = 0
    num_groups = len(groups)

    for row in range(nrows):
        for col in range(ncols):
            if group_index < num_groups:
                # Read in data to a dataframe for each stat group. Change the dataframe index to year. Select only the columns for the stats provided. All stats will be recast to type float for any calculations later.
                df_index = 'Year'
                groups[group_index].prepare_dataframe(df_index)

                # Calculate the percent change of each stat each year relative to the reference averages.
                groups[group_index].calculate_percent_change(ref_year_start, ref_year_end)

                # Plot percent changes in each stat by year for each stat group.
                groups[group_index].plot_by_year(axes[row, col], ref_year_start, ref_year_end)
                
                group_index += 1

    plt.show()

def main():
    # Create stat groups for batting, pitching, fielding, and misc.
    batting_name = 'Batting'
    batting_file = 'batting_yearly_averages.csv'
    batting_stats = ['R', 'H', '1B', '2B', '3B', 'HR', 'RBI', 'TB', 'BB', 'SO', 'SH', 'SB', 'BA', 'OBP', 'SLG', 'OPS']
    batting = statGroup(batting_name, batting_file, batting_stats)

    pitching_name = 'Pitching'
    pitching_file = 'pitching_yearly_averages.csv'
    pitching_stats = ['R', 'ER', 'H', 'HR', 'BB', 'SO', 'ERA', 'WHIP', 'BAbip']
    pitching = statGroup(pitching_name, pitching_file, pitching_stats)

    fielding_name = 'Fielding'
    fielding_file = 'fielding_yearly_averages.csv'
    fielding_stats = ['Ch', 'A', 'PO', 'E', 'DP', 'Fld%', 'SB', 'CS', 'CS%']
    fielding = statGroup(fielding_name, fielding_file, fielding_stats)

    misc_name = 'Misc'
    misc_file = 'misc_yearly_averages.csv'
    misc_stats = ['R/G', 'PA/G', 'Batters/G', 'Pitchers/G', 'PH/G', 'PR/G']
    misc = statGroup(misc_name, misc_file, misc_stats)

    # Choose which stat groups to plot. Define a reference year range to calculate percent changes of each stat relative to the average of the reference year range. This allows for a comparison of how drastically each stat has changed over time.
    groups_to_plot = [batting, pitching, fielding, misc]
    ref_year_start = 1908
    ref_year_end = 1919
    plot_stats_by_year(groups_to_plot, ref_year_start, ref_year_end)

if __name__ == "__main__":
    main()