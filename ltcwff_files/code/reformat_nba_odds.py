# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 14:34:18 2021

@author: Harry
"""

from os import path
import pandas as pd

DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'

teams = {'Atlanta': 'ATL', 'Boston': 'BOS', 'Brooklyn': 'BRK', 'Charlotte': 'CHO', 'Chicago': 'CHI', 'Cleveland': 'CLE', 'Dallas': 'DAL', 'Denver': 'DEN', 'Detroit': 'DET', 'GoldenState': 'GSW', 'Houston': 'HOU', 'Indiana': 'IND', 'LAClippers': 'LAC', 'LALakers': 'LAL', 'Memphis': 'MEM', 'Miami': 'MIA', 'Milwaukee': 'MIL', 'Minnesota': 'MIN', 'NewOrleans': 'NOP', 'NewYork': 'NYK', 'OklahomaCity': 'OKC', 'Orlando': 'ORL', 'Philadelphia': 'PHI', 'Phoenix': 'PHO', 'Portland': 'POR', 'Sacramento': 'SAC', 'SanAntonio': 'SAS', 'Toronto': 'TOR', 'Utah': 'UTA', 'Washington': 'WAS'}

raw_odds_data = pd.read_csv(path.join(DATA_DIR, 'nba_odds_2020-21.csv'))

raw_odds_data

odds_data = raw_odds_data[['Date', 'Team', 'Open', 'Close', 'ML', '2H']]

odds_data['Team'] = [ teams[team] for team in odds_data['Team'] ]
odds_data

odds_data_formatted = []

i = 0
while i < len(odds_data.index):
    row = {}
    favorite = float(odds_data.loc[odds_data.index[i], 'Open']) > 100
    row['Date'] = odds_data.loc[odds_data.index[i], 'Date']
    row['Favorite'] = odds_data.loc[odds_data.index[i + favorite], 'Team']
    row['Underdog'] = odds_data.loc[odds_data.index[i + (not favorite)], 'Team']
    row['Spread Open'] = odds_data.loc[odds_data.index[i + favorite], 'Open']
    row['Spread Close'] = odds_data.loc[odds_data.index[i + favorite], 'Close']
    row['Total Open'] = odds_data.loc[odds_data.index[i + (not favorite)], 'Open']
    row['Total Close'] = odds_data.loc[odds_data.index[i + (not favorite)], 'Close']
    row['Fav ML'] = odds_data.loc[odds_data.index[i + favorite], 'ML']
    row['Dog ML'] = odds_data.loc[odds_data.index[i + (not favorite)], 'ML']
    favorite_2H = float(odds_data.loc[odds_data.index[i], '2H']) > 50
    row['2H Favorite'] = odds_data.loc[odds_data.index[i + favorite_2H], 'Team']
    row['2H Underdog'] = odds_data.loc[odds_data.index[i + (not favorite_2H)], 'Team']
    row['2H Spread'] = odds_data.loc[odds_data.index[i + favorite_2H], '2H']
    row['2H Total'] = odds_data.loc[odds_data.index[i + (not favorite_2H)], '2H']
    #print(row)
    if row['Spread Open'] == 'pk':
        row['Spread Open'] = '0'
    if row['Spread Close'] == 'pk':
        row['Spread Close'] = '0'
    if row['2H Spread'] == 'pk':
        row['2H Spread'] = '0'
    odds_data_formatted.append(row)
    i += 2

odds_data_formatted = pd.DataFrame(odds_data_formatted)
print(odds_data_formatted)
odds_data_formatted.to_csv(path.join(DATA_DIR, 'odds_data_formatted.csv'))
