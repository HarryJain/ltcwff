import pandas as pd
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'

adp = pd.read_csv(path.join(DATA_DIR, 'adp_2017.csv'))  # adp data

adp.mean()
adp.max()
# Added by Harry
adp.min()
adp.std()
adp.count()
adp.sum()

# Axis
adp[['adp', 'low', 'high', 'stdev']].mean(axis=0)
adp[['adp', 'low', 'high', 'stdev']].mean(axis=1).head()

# Summary functions on boolean columns
pg = pd.read_csv(path.join(DATA_DIR, 'player_game_2017_sample.csv'))
pg['good_rb_game'] = (pg['pos'] == 'RB') & (pg['rush_yards'] >= 100)

pg['good_rb_game'].mean()
pg['good_rb_game'].sum()

pg[['pass_yards', 'rush_yards']] > 400

(pg['pass_yards'] > 400).any()
(pg['rush_yards'] >= 0).all()

(pg[['rush_yards', 'rec_yards']] > 100).any(axis=1)

(pg[['rush_yards', 'rec_yards']] > 100).any(axis=1).sum()

(pg[['rush_yards', 'rec_yards']] > 100).all(axis=1).sum()

(pg[['rush_yards', 'rec_yards']] > 75).all(axis=1).sum()

# Other misc built-in summary functions
adp['position'].value_counts()

pd.crosstab(adp['team'], adp['position']).head()

###########
# Exercises
###########

# 3.2.1
# ANS:
pg = pd.read_csv(path.join(DATA_DIR, 'player_game_2017_sample.csv'))
# ANS2:
pg = pd.read_csv(path.join(DATA_DIR, 'player_game_2017_sample.csv'))
# TEST:
pg.head()

# 3.2.2
# ANS:
pg['total_yards1'] = pg['rush_yards'] + pg['rec_yards']
# ANS2:
pg['total_yards1'] = pg['rush_yards'] + pg['rec_yards'] + pg['pass_yards']
pg['total_yards2'] = pg[['rush_yards', 'rec_yards', 'pass_yards']].sum(axis = 1)
# TEST:
pg['total_yards1']
pg['total_yards2']

# 3.2.3
# a)
pg[['rush_yards', 'rec_yards']].mean()
# b)
((pg['pass_yards'] >= 300) & (pg['pass_tds'] >= 3)).sum()
# c)
((pg['pass_yards'] >= 300) & (pg['pass_tds'] >= 3)).sum() / (pg['pos'] == 'QB').sum()
# d)
pg['rush_tds'].sum()
# e)
# Most = 14
pg['week'].value_counts().idxmax()
# Least = 8
pg['week'].value_counts().idxmin()
# TEST:
pg['week'].value_counts()
