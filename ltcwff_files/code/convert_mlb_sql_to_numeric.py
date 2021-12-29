# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 15:00:17 2021

@author: Harry
"""

# Module Imports
import pandas as pd
import sqlite3
from os import path


# Data directory for csv files
DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'


# Open database connection
conn = sqlite3.connect(path.join(DATA_DIR, 'mlb.sqlite'))


# Get whole games table and rewrite it with all possible columns as numeric values
games = pd.read_sql('''SELECT * FROM games''', conn)
games = games.set_index('game_id')
print(games)

text_cols = ['game_id', 'Date', 'Away Team', 'Home Team', 'Away SP', 'Home SP', 'WP', 'WP Record', 'LP', 'LP Record', 'SV']
int_cols = ['Away 1', 'Home 1', 'Away 2', 'Home 2', 'Away 3', 'Home 3', 'Away 4', 'Home 4', 'Away 5', 'Home 5', 'Away 6', 'Home 6', 'Away 7', 'Home 7', 'Away 8', 'Home 8', 'Away 9', 'Home 9', 'Away 10', 'Home 10', 'Away 11', 'Home 11', 'Away 12', 'Home 12', 'Away 13', 'Home 13', 'Away R', 'Home R', 'Away H', 'Home H', 'Away E', 'Home E', 'SV Count']
real_cols = []

col_types = { col: ('INT' if col in int_cols else 'REAL' if col in real_cols else 'TEXT') for col in list(games.columns) }

games.to_sql('new_games', conn, if_exists = 'replace', dtype = col_types)


# Commit the database changes and close it
conn.commit()
conn.close()
