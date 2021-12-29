import pandas as pd
import numpy as np
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'

pg = pd.read_csv(path.join(DATA_DIR, 'player_game_2017_sample.csv'))  # player-game
games = pd.read_csv(path.join(DATA_DIR, 'game_2017_sample.csv'))  # game info
pg.head()
games.head()

# things to care about while merging:
# 1. The columns you're joining on.
pd.merge(pg, games[['gameid', 'home', 'away']]).head()

rush_df = pg[['gameid', 'player_id', 'rush_yards', 'rush_tds']]
rec_df = pg[['gameid', 'player_id', 'rec_yards', 'rec_tds']]

combined = pd.merge(rush_df, rec_df, on=['player_id', 'gameid'])
combined.head()

# 2. Whether you're doing a one-to-one, one-to-many, or many-to-many merge
player = pd.read_csv(path.join(DATA_DIR, 'player_2017_sample.csv')) # player info
player

player['player_id'].duplicated().any()

pg['player_id'].duplicated().any()
pg['player_id'].duplicated().sum()

pd.merge(combined, player).head()

pd.merge(player, combined, validate = '1:m')
# pd.merge(combined, player, validate='1:m')  # this will fail since it's 1:m
# pd.merge(combined, player, validate='1:1')  # this will fail since it's 1:m

# 3. What you do with unmatched observations
rush_df = pg.loc[pg['rush_yards'] > 0,
       ['gameid', 'player_id', 'rush_yards', 'rush_tds']]
rush_df

rec_df = pg.loc[pg['rec_yards'] > 0,
          ['gameid', 'player_id', 'rec_yards', 'rec_tds']]
rec_df

rush_df.shape
rec_df.shape

comb_inner = pd.merge(rush_df, rec_df)
comb_inner.shape
comb_inner.sample(5)

comb_left = pd.merge(rush_df, rec_df, how='left')
comb_left.shape
comb_left.sample(5)

comb_outer = pd.merge(rush_df, rec_df, how='outer', indicator=True)
comb_outer.shape
comb_outer.sample(5)

comb_outer['_merge'].value_counts()

# More on pd.merge
# left_on and right_on
rush_df = pg.loc[pg['rush_yards'] > 0,
                 ['gameid', 'player_id', 'rush_yards', 'rush_tds']]
rush_df.columns = ['gameid', 'rb_id', 'rush_yards', 'rush_tds']

pd.merge(rush_df, rec_df, left_on=['gameid', 'rb_id'],
    right_on=['gameid', 'player_id']).head()

# merging on index
max_rush_df = rush_df.groupby('rb_id')[['rush_yards', 'rush_tds']].max()
max_rush_df.head()
max_rush_df.sample(5)

max_rush_df.columns = [f'max_{x}' for x in max_rush_df.columns]
max_rush_df.columns

pd.merge(rush_df, max_rush_df, left_on='rb_id', right_index=True).head()

#############
# pd.concat()
#############
rush_df = (pg.loc[pg['rush_yards'] > 0,
                  ['gameid', 'player_id', 'rush_yards', 'rush_tds']]
           .set_index(['gameid', 'player_id']))
rush_df
rec_df = (pg.loc[pg['rec_yards'] > 0,
                 ['gameid', 'player_id', 'rec_yards', 'rec_tds']]
          .set_index(['gameid', 'player_id']))
rec_df

pd.concat([rush_df, rec_df], axis=1).head()

pass_df = (pg.loc[pg['pass_yards'] > 0,
                  ['gameid', 'player_id', 'pass_yards', 'pass_tds']]
           .set_index(['gameid', 'player_id']))

pd.concat([rush_df, rec_df, pass_df], axis=1).head()

adp = pd.read_csv(path.join(DATA_DIR, 'adp_2017.csv'))  # adp data

qbs = adp.loc[adp['position'] == 'QB']
rbs = adp.loc[adp['position'] == 'RB']

qbs.shape
rbs.shape

pd.concat([qbs, rbs]).shape
pd.concat([qbs, rbs]).sample(5)

###########
# Exercises
###########

# 3.5.1
# ANS:
# a)
df_touch = pd.read_csv(path.join(DATA_DIR, 'problems\\combine1', 'touch.csv'))
df_yard = pd.read_csv(path.join(DATA_DIR, 'problems\\combine1', 'yard.csv'))
df_td = pd.read_csv(path.join(DATA_DIR, 'problems\\combine1', 'td.csv'))
# b)
df_comb1 = pd.merge(df_touch, df_yard)
df_comb1 = pd.merge(df_comb1, df_td, how = 'left')
df_comb1[['rush_tds', 'rec_tds']] = df_comb1[['rush_tds', 'rec_tds']].fillna(0)
# TEST:
df_comb1
# c)
df_comb2 = pd.concat([df_touch.set_index('id'), df_yard.set_index('id'), df_td.set_index('id')], axis = 1)
df_comb2[['rush_tds', 'rec_tds']] = df_comb2[['rush_tds', 'rec_tds']].fillna(0)
# TEST:
df_comb2
# d) pd.concat is better since it can combine 3 at once, though pd.merge gives more control

# 3.5.2
# a)
qb = pd.read_csv(path.join(DATA_DIR, 'problems\\combine2', 'qb.csv'))
rb = pd.read_csv(path.join(DATA_DIR, 'problems\\combine2', 'rb.csv'))
wr = pd.read_csv(path.join(DATA_DIR, 'problems\\combine2', 'wr.csv'))
te = pd.read_csv(path.join(DATA_DIR, 'problems\\combine2', 'te.csv'))
# TEST:
qb.head()
rb.head()
wr.head()
te.head()
# b)
df = pd.concat([qb, rb, wr, te])
# TEST:
df

# 3.5.3
# a)
adp = pd.read_csv(path.join(DATA_DIR, 'adp_2017.csv'))
# TEST:
adp.head()
# b)
positions = adp['position'].drop_duplicates().to_list()
for pos in positions:
    adp.loc[adp['position'] == pos].to_csv(path.join(DATA_DIR, f'adp_{pos}.csv'), index = False)
# c)
df = pd.concat([ pd.read_csv(path.join(DATA_DIR, f'adp_{pos}.csv')) for pos in positions ], ignore_index = True)
# TEST:
df