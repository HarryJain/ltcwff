# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 22:01:52 2021

@author: Harry
"""

# Module Imports
import pandas as pd
import sqlite3
from os import path


# Data directory for csv files
DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'


# Open database connection
conn = sqlite3.connect(path.join(DATA_DIR, 'nba.sqlite'))


# Get whole game table and rewrite it with all possible columns as numeric values
player_games = pd.read_sql('''SELECT * FROM player_games''', conn)
player_games = player_games.set_index('player_id')
print(player_games)

text_cols = ['player_id', 'game_id', 'MP']
int_cols = ['FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', '+/-',]
real_cols = ['FG%', '3P%', 'FT%', 'TS%', 'eFG%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%', 'ORtg', 'DRtg', 'BPM']

col_types = { col: ('INT' if col.split(' ')[-1] in int_cols else 'REAL' if col.split(' ')[-1] in real_cols else 'TEXT') for col in list(player_games.columns) }
player_games.to_sql('new_player_games', conn, if_exists = 'replace', dtype = col_types)


# Commit the database changes and close it
conn.commit()
conn.close()
