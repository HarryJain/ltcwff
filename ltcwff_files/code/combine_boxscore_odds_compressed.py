# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 16:15:49 2021

@author: Harry
"""


# Module imports
from os import path
import pandas as pd


# Global Variables
DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'
teams = {'Atlanta': 'ATL', 'Boston': 'BOS', 'Brooklyn': 'BRK', 'Charlotte': 'CHO', 'Chicago': 'CHI', 'Cleveland': 'CLE', 'Dallas': 'DAL', 'Denver': 'DEN', 'Detroit': 'DET', 'Golden State': 'GSW', 'Houston': 'HOU', 'Indiana': 'IND', 'LA': 'LAC', 'L.A. Lakers': 'LAL', 'LA Lakers': 'LAL', 'LA Clippers': 'LAC', 'L.A. Clippers': 'LAC', 'Memphis': 'MEM', 'Miami': 'MIA', 'Milwaukee': 'MIL', 'Minnesota': 'MIN', 'New Orleans': 'NOP', 'New York': 'NYK', 'Oklahoma City': 'OKC', 'Orlando': 'ORL', 'Philadelphia': 'PHI', 'Phoenix': 'PHO', 'Portland': 'POR', 'Sacramento': 'SAC', 'San Antonio': 'SAS', 'Toronto': 'TOR', 'Utah': 'UTA', 'Washington': 'WAS'}


# Open and format odds
odds = pd.read_csv(path.join(DATA_DIR, 'scraped_odds_data_2021_compressed.csv'))
odds = odds.drop(odds.columns[0], axis = 1)
odds['Home Team'] = [ teams[team] for team in odds['Home Team'] ]
odds['Away Team'] = [ teams[team] for team in odds['Away Team'] ]
odds['Index'] = [ f"{odds.loc[ind, 'Date']}_{odds.loc[ind, 'Home Team']}_{odds.loc[ind, 'Away Team']}" for ind in odds.index ]
odds = odds.set_index('Index')
odds


# Open and format boxscores
boxscores = pd.read_csv(path.join(DATA_DIR, 'scraped_nba_boxscores_2021_compressed.csv'))
boxscores = boxscores.drop(boxscores.columns[0], axis = 1)
boxscores['Home Team'] = [ teams[team] for team in boxscores['Home Team'] ]
boxscores['Away Team'] = [ teams[team] for team in boxscores['Away Team'] ]
boxscores['Index'] = [ f"{boxscores.loc[ind, 'Date']}_{boxscores.loc[ind, 'Home Team']}_{boxscores.loc[ind, 'Away Team']}" for ind in boxscores.index ]
boxscores = boxscores.set_index('Index')
boxscores


# Combine tables
combined = pd.concat([boxscores, odds], axis = 1, join = 'inner')
combined = combined.loc[:, ~combined.columns.duplicated()]
print(combined)

combined.to_csv(path.join(DATA_DIR, 'scraped_nba_combined_2021_compressed.csv'))
