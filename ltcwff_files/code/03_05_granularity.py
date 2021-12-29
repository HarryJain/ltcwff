import pandas as pd
import numpy as np
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'

pbp = pd.read_csv(path.join(DATA_DIR, 'play_data_sample.csv'))  # play by play data
pbp.head()
pbp.columns
pbp.shape

((pbp['rush_attempt'] == True) & (pbp['yards_gained'] > 5)).mean()

# Granularity

# Grouping
pbp.groupby('game_id').sum()
pbp.groupby('game_id').sum().reset_index()
pbp.groupby('game_id', as_index = False).sum()

sum_cols = ['yards_gained', 'rush_attempt', 'pass_attempt', 'shotgun']
pbp.groupby('game_id').sum()[sum_cols]

pbp.groupby('game_id').agg({'yards_gained': 'sum', 'play_id':
    'count', 'interception': 'sum', 'touchdown': 'sum'})

pbp.groupby('game_id').agg(
    yards_gained = ('yards_gained', 'sum'),
    nplays = ('play_id', 'count'),
    interception = ('interception', 'sum'),
    touchdown = ('touchdown', 'sum'))

pbp.groupby('game_id').agg({'yards_gained': ['sum', 'mean']})

yards_per_team_game = pbp.groupby(
         ['game_id', 'posteam']).agg({'yards_gained': ['sum', 'mean']})

yards_per_team_game

# A note on multilevel indexing
yards_per_team_game.loc[[(2018101412, 'NE'), (2018111900, 'LA')]]

# Stacking and unstacking data
pg = pd.read_csv(path.join(DATA_DIR, 'player_game_2017_sample.csv'))

qbs = pg.loc[pg['pos'] == 'QB', ['player_name', 'week', 'pass_tds']]
qbs.sample(5)

qbs_reshaped = qbs.set_index(['player_name', 'week']).unstack()
qbs_reshaped.head()

total_tds = qbs_reshaped.sum(axis=1).head()
total_tds.sort_values(ascending = False)

qbs_reshaped.stack().head()

###########
# Exercises
###########

# 3.4.1
# ANS: Shifting granularity by grouping (fine-grained to coarse-grained) causes loss of information, as we cannot later unpack it, while stacking/unstacking/reshaping does not change the amount of information, merely rearranges it

# 3.4.2
# a)
pbp = pd.read_csv(path.join(DATA_DIR, 'play_data_sample.csv'))
# TEST:
pbp.sample(5)
# b) Sony Michel with 106 yards in game 2018101412 and Kareem Hunt with 70 yards in game 2018111900
# Numbers and names
pbp.loc[pbp['play_type'] == 'run'].groupby(['game_id', 'rusher_player_name'])['yards_gained'].sum().to_frame().sort_values(['game_id', 'yards_gained'], ascending = False).groupby('game_id').head(1)
pbp.loc[pbp['play_type'] == 'run'].groupby(['game_id', 'rusher_player_name'])['yards_gained'].sum().reset_index().groupby('game_id').apply(lambda x: x.loc[x['yards_gained'].idxmax()]).drop('game_id', axis = 1)
# Only numbers
pbp.loc[pbp['play_type'] == 'run'].groupby(['game_id', 'rusher_player_name'])['yards_gained'].sum().reset_index().groupby('game_id')['yards_gained'].max()
pbp.loc[pbp['play_type'] == 'run'].groupby(['game_id', 'rusher_player_name'])['yards_gained'].sum().max(level = 'game_id')
# TEST:
pbp.columns
# c)
# YPC per game
pbp.loc[pbp['play_type'] == 'run'].groupby(['game_id', 'rusher_player_name'])['yards_gained'].mean()
# YPC for all games
pbp.loc[pbp['play_type'] == 'run'].groupby('rusher_player_name')['yards_gained'].mean()
# d)
pbp.loc[pbp['play_type'] == 'run'].groupby(['game_id', 'rusher_player_name']).apply(lambda x: (x['yards_gained'] <= 0).mean())
# Solution:
pbp['lte_0_yards'] = pbp['yards_gained'] <= 0
pbp.query("play_type == 'run'").groupby(['game_id', 'rusher_player_name'])['lte_0_yards'].mean()

# 3.4.3
# TEST:
pbp.groupby('game_id').count()
pbp.groupby('game_id').sum()
# ANS: Count gives the number of non-null values for that game, while sum does a numeric sum of the columns where possible; they would only give the same result for a column of all 1s or some other numeric data that sums to the number of items

# 3.4.4
# ANS (misinterpreted):
pbp.groupby('game_id').apply(lambda x: x['first_down'].mean())
pbp.groupby('posteam').apply(lambda x: x['first_down'].mean())
pbp.groupby('game_id').apply(lambda x: x['turnover'].mean())
pbp.groupby('posteam').apply(lambda x: x['turnover'].mean())
# Solution: Pats First Down (31.25%) and Chiefs vs. Rams Turnover (6.85%)
pbp.groupby(['posteam', 'game_id'])['turnover', 'first_down'].mean()
# TEST:
pbp.columns

# 3.5.5
# ANS: Stacking and unstacking doesn't change the amount of information in the data, just reshapes it
