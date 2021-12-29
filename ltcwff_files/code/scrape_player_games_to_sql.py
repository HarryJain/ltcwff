# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 17:12:00 2021

@author: Harry
"""

# Module Imports
from bs4 import BeautifulSoup as Soup
from sys import exit
from os import path
import requests
from pandas import DataFrame
import pandas as pd
from time import sleep
from datetime import date
import sqlite3


# Global Variables
DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'
team_dict = {'Atlanta': 'ATL', 'Boston': 'BOS', 'Brooklyn': 'BRK', 'Charlotte': 'CHO', 'Chicago': 'CHI', 'Cleveland': 'CLE', 'Dallas': 'DAL', 'Denver': 'DEN', 'Detroit': 'DET', 'Golden State': 'GSW', 'Houston': 'HOU', 'Indiana': 'IND', 'LA': 'LAC', 'L.A. Lakers': 'LAL', 'LA Lakers': 'LAL', 'LA Clippers': 'LAC', 'L.A. Clippers': 'LAC', 'Memphis': 'MEM', 'Miami': 'MIA', 'Milwaukee': 'MIL', 'Minnesota': 'MIN', 'New Orleans': 'NOP', 'New York': 'NYK', 'Oklahoma City': 'OKC', 'Orlando': 'ORL', 'Philadelphia': 'PHI', 'Phoenix': 'PHO', 'Portland': 'POR', 'Sacramento': 'SAC', 'San Antonio': 'SAS', 'Toronto': 'TOR', 'Utah': 'UTA', 'Washington': 'WAS'}
BASE_URL = 'https://www.basketball-reference.com'


# Return the soup for the boxscores for a given game "link"/site path
def get_soup(link):
    url = BASE_URL + link
    print(url)
    response = requests.get(url)
    if not 200 <= response.status_code < 300:
        exit('Invalid Link')
    return Soup(response.content, 'html.parser')


# Return a list of elements in a table row
def parse_row(row):
    # result = [ x.string if x.find('a') == None else x.find('a').string for x in row.find_all('td') ]
    result = [ x.string for x in row.find_all('td') ]
    return result


# Convert a web data table to a DataFrame, with an option to deal with an overheader
def table_to_df(table, overheader = 0):
    cols = table.find('thead').find_all('tr')[overheader].find_all('th')
    cols = [ col.string if col.string != None else '' for col in cols ][1:]
    
    stat_table = table.find('tbody')
        
    rows = stat_table.find_all('tr')
    
    headers = [ row.find('th').get('data-append-csv') if row.find('th').get('data-append-csv') != None else row.find('a').get('href').split('/')[-1].split('.')[0] for row in rows if row.find('th') != None and row.find('th').string != 'Reserves' ]
    
    list_of_parsed_rows = [ parse_row(row) for row in rows[0:len(rows)] ]
    list_of_parsed_rows = [ row for row in list_of_parsed_rows if row != [] ]
    list_of_parsed_rows
    
    df = DataFrame(list_of_parsed_rows)
    
    if len(headers) != 0:
        df.index = headers
        df.index.name = 'player_id'
        
    if len(df.columns) == 1:
        old_df = df
        df = df.reindex(columns = cols)        
        df.iloc[:, 0] = old_df.iloc[:, 0]
        print(df)
    else:
        df.columns = cols
    
    return df


# Return a DataFrame with all the player stats for a given game
def get_game_data(row):
    soup = get_soup(f"/boxscores/{row['game_id']}.html")
    
    table_types = ['game-basic', 'game-advanced', 'q1-basic', 'q2-basic', 'h1-basic', 'q3-basic', 'q4-basic', 'h2-basic']
    home_dfs = []
    away_dfs = []

    for table_type in table_types:
        home = soup.find('table', {'id': f'box-{row["Home Team"]}-{table_type}'})
        away = soup.find('table', {'id': f'box-{row["Away Team"]}-{table_type}'})
        if home == None or away == None:
            return
        home = table_to_df(home, True)
        away = table_to_df(away, True)
        if table_type == 'game-advanced':
            home = home.drop('MP', axis = 1)
            away = away.drop('MP', axis = 1)
        elif not 'game' in table_type:
            home.columns = [ table_type.split('-')[0].upper() + ' ' + col for col in home.columns ]
            away.columns = [ table_type.split('-')[0].upper() + ' ' + col for col in away.columns ]
        home_dfs.append(home)
        away_dfs.append(away)
            
    home_df = pd.concat(home_dfs, axis = 1)
    away_df = pd.concat(away_dfs, axis = 1)
    
    combined = pd.concat([home_df, away_df])
    combined.insert(0, 'game_id', row['game_id'])
    return combined


# Connect to the database and get a DataFrame of game data
conn = sqlite3.connect(path.join(DATA_DIR, 'nba.sqlite'))
game_rows = pd.read_sql('SELECT game_id, "Home Team", "Away Team" FROM games', conn)


# If you are adding to player_games, populate the dfs list with the current table
try:
    player_game_rows = pd.read_sql('SELECT DISTINCT game_id FROM player_games', conn)
    completed_game_ids = list(player_game_rows['game_id'])
    
    todo_game_rows = game_rows.loc[~game_rows['game_id'].isin(completed_game_ids)]
    todo_game_rows
    
    player_games = pd.read_sql('SELECT * FROM player_games', conn)
    player_games = player_games.set_index('player_id')
    
    dfs = [player_games]
    new_dfs = []
# If you are starting without a player_games table, create an empty dfs list
except:
    todo_game_rows = game_rows
    dfs = []
    new_dfs = []


# Scrape 1000 (or the remaining amount) of game boxscore DataFrames and add them to the dfs list
for i in range(min(1000, len(todo_game_rows))):
    print(i)
    df = get_game_data(todo_game_rows.iloc[i])
    #df = df.replace('\xa0', 'Did Not Play')
    print(df)
    dfs.append(df)
    new_dfs.append(df)
    sleep(1)


# Combine the game DataFrames and write the combined DataFrame to the database (and a backup csv)
big_df = pd.concat(dfs)
print(big_df)
big_df.to_sql('player_games', conn, if_exists = 'replace')
big_df.to_csv(path.join(DATA_DIR, f'player_games.csv'))


# Commit the database changes and close it
conn.commit()
conn.close()