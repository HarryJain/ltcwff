# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 17:17:13 2021

@author: Harry
"""

# Module Imports
import pandas as pd
import sqlite3
import os
from os import path
from datetime import date


# Data directory for csv files
DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'

# Dictionary relating prop names to stats
stat_dict = {'Points': 'PTS', 'Assists': 'AST', 'Rebounds': 'TRB', 'Reb + Ast': 'TRB + AST', 'Made Threes': '3P', 'Pts + Ast': 'PTS + AST', 'Pts + Reb': 'PTS + TRB', 'Pts + Reb + Ast': 'PTS + TRB + AST'}

# Open database connection
conn = sqlite3.connect(path.join(DATA_DIR, 'nba.sqlite'))

# Get today's date in our format and print it out
today = date.today()
datef = today.strftime("%Y%m%d")
print(datef)

# Load prop data for today into a DataFrame
try:
    props_df = pd.read_csv(path.join(DATA_DIR, 'player_props', f'{datef}.csv'))
except:
    os.system('python new_get_player_props.py')
    props_df = pd.read_csv(path.join(DATA_DIR, f'{datef}.csv'))

# Clean prop table by dropping old index column and converting columns to numeric
props_df = props_df.drop(props_df.columns[0], axis = 1)
for col in props_df.columns:
    try:
        props_df[col] = pd.to_numeric(props_df[col])
    except:
        continue

# Loop through each row of the props DataFrame
for ind in props_df.index:
    # Get the prop name to use in the query as well as the player name
    prop_parts = stat_dict[props_df.loc[ind, 'Prop']].split(' + ')
    prop_name = f'''"{'" + "'.join(prop_parts)}"'''
    player = props_df.loc[ind, 'Player']
    
    # Get the player's table for that prop
    table = pd.read_sql(f'''SELECT {prop_name} FROM player_games JOIN games ON player_games.game_id = games.game_id WHERE player_id = "{player}" AND Season = "2020-21" AND Playoffs = 1''', conn)
    for col in table.columns:
        try:
            table[col] = pd.to_numeric(table[col], errors='coerce')
        except:
            continue
    
    # Reset the prop name for single props
    if len(prop_parts) == 1:
        prop_name = prop_name[1:len(prop_name) - 1]
    
    # Create average and cover columns
    props_df.loc[ind, 'Playoff Avg'] = table[prop_name].mean()
    props_df.loc[ind, 'Playoff Cover %'] = (table[prop_name] > props_df.loc[ind, 'Over']).mean()
    props_df.loc[ind, 'Finals Avg'] = table[-4:][prop_name].mean()
    props_df.loc[ind, 'Finals Cover %'] = (table.iloc[-4:][prop_name] > props_df.loc[ind, 'Over']).mean()

# Print the extreme cover values
print(props_df[(props_df['Playoff Cover %'] > 0.5) & (props_df['Finals Cover %'] > 0.5)])
    
# Close the database
conn.close()