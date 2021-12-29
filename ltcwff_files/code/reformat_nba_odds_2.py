# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 19:07:17 2021

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
for ind in odds_data.index:
    if odds_data.loc[ind, 'Open'] == 'pk':
        odds_data.loc[ind, 'Open'] = 0
    if odds_data.loc[ind, 'Close'] == 'pk':
        odds_data.loc[ind, 'Close'] = 0
    if odds_data.loc[ind, '2H'] == 'pk':
        odds_data.loc[ind, '2H'] = 0
odds_data

odds_data_formatted = []
teams = []

i = 0
while i < len(odds_data.index):
    row_1 = {}
    row_2 = {}
    favorite = float(odds_data.loc[odds_data.index[i], 'Open']) > 100
    row_1['Date'] = odds_data.loc[odds_data.index[i], 'Date']
    row_2['Date'] = odds_data.loc[odds_data.index[i], 'Date']
    favorite_team = odds_data.loc[odds_data.index[i + favorite], 'Team']
    underdog_team = odds_data.loc[odds_data.index[i + (not favorite)], 'Team']
    row_1['Team'] = favorite_team
    row_2['Team'] = underdog_team
    row_1['Spread Open'] = -float(odds_data.loc[odds_data.index[i + favorite], 'Open'])
    row_1['Spread Close'] = -float(odds_data.loc[odds_data.index[i + favorite], 'Close'])
    row_2['Spread Open'] = odds_data.loc[odds_data.index[i + favorite], 'Open']
    row_2['Spread Close'] = odds_data.loc[odds_data.index[i + favorite], 'Close']
    row_1['Total Open'] = odds_data.loc[odds_data.index[i + (not favorite)], 'Open']
    row_1['Total Close'] = odds_data.loc[odds_data.index[i + (not favorite)], 'Close']
    row_2['Total Open'] = odds_data.loc[odds_data.index[i + (not favorite)], 'Open']
    row_2['Total Close'] = odds_data.loc[odds_data.index[i + (not favorite)], 'Close']
    row_1['ML'] = odds_data.loc[odds_data.index[i + favorite], 'ML']
    row_2['ML'] = odds_data.loc[odds_data.index[i + (not favorite)], 'ML']
    favorite_2H = float(odds_data.loc[odds_data.index[i], '2H']) > 50
    fav_mult = 1
    dog_mult = 1
    if odds_data.loc[odds_data.index[i + favorite_2H], 'Team'] == favorite_team:
        dog_mult = -1
    else:
        fav_mult = -1
    #row['2H Favorite'] = odds_data.loc[odds_data.index[i + favorite_2H], 'Team']
    #row['2H Underdog'] = odds_data.loc[odds_data.index[i + (not favorite_2H)], 'Team']
    row_1['2H Spread'] = fav_mult * float(odds_data.loc[odds_data.index[i + favorite_2H], '2H'])
    row_2['2H Spread'] = dog_mult * float(odds_data.loc[odds_data.index[i + favorite_2H], '2H'])
    row_1['2H Total'] = odds_data.loc[odds_data.index[i + (not favorite_2H)], '2H']
    row_2['2H Total'] = odds_data.loc[odds_data.index[i + (not favorite_2H)], '2H']
    #print(row)
    '''
    if row['Spread Open'] == 'pk':
        row['Spread Open'] = '0'
    if row['Spread Close'] == 'pk':
        row['Spread Close'] = '0'
    if row['2H Spread'] == 'pk':
        row['2H Spread'] = '0'
    '''
    odds_data_formatted.append(row_1)
    odds_data_formatted.append(row_2)
    #teams.append(favorite_team)
    #teams.append(underdog_team)
    i += 2

odds_data_formatted = pd.DataFrame(odds_data_formatted)
print(odds_data_formatted)
odds_data_formatted.to_csv(path.join(DATA_DIR, 'odds_data_formatted_2.csv'))
