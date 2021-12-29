import pandas as pd
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'

# load data
pg = pd.read_csv(path.join(DATA_DIR, 'player_game_2017_sample.csv'))

pg['pts_pr_pass_td'] = 4
pg[['gameid', 'player_id', 'pts_pr_pass_td']].head()

pg['pts_pr_pass_td'] = 6
pg[['gameid', 'player_id', 'pts_pr_pass_td']].head()

# Math and number columns
pg['rushing_pts'] = (
    pg['rush_yards']*0.1 + pg['rush_tds']*6 + pg['rush_fumbles']*-3)

pg[['player_name', 'gameid', 'rushing_pts']].head()

import numpy as np  # note: normally you'd import this at the top of the file

pg['distance_traveled'] = np.abs(pg['rush_yards'])

pg['ln_rush_yds'] = np.log(pg['rush_yards'])

# note on sample method

pg['points_per_fg'] = 3

pg[['player_name', 'gameid', 'points_per_fg']].sample(5)

# String Columns
pg['player_name'].str.upper().sample(5)

pg['player_name'].str.replace('.', ' ').sample(5)

(pg['player_name'] + ', ' + pg['pos'] + ' - ' + pg['team']).sample(5)

pg['player_name'].str.replace('.', ' ').str.lower().sample(5)

# Bool columns
pg['is_a_rb'] = (pg['pos'] == 'RB')
pg[['player_name', 'is_a_rb']].sample(5)

pg['is_a_rb_or_wr'] = (pg['pos'] == 'RB') | (pg['pos'] == 'WR')
pg['good_rb_game'] = (pg['pos'] == 'RB') & (pg['rush_yards'] >= 100)
pg['is_not_a_rb_or_wr'] = ~((pg['pos'] == 'RB') | (pg['pos'] == 'WR'))

(pg[['rush_yards', 'rec_yards']] > 100).sample(5)

# Applying functions to columns
def is_skill(pos):
  """
  Takes some string named pos ('QB', 'K', 'RT' etc) and checks
  whether it's a skill position (RB, WR, TE).
  """
  return pos in ['RB', 'WR', 'TE']

pg['is_skill'] = pg['pos'].apply(is_skill)

pg[['player_name', 'is_skill']].sample(5)

pg['is_skill_alternate'] = pg['pos'].apply(lambda x: x in ['RB', 'WR', 'TE'])

# Dropping Columns
pg.drop('is_skill_alternate', axis=1, inplace=True)

# Renaming Columns
pg.columns = [x.upper() for x in pg.columns]

pg.head()

pg.columns = [x.lower() for x in pg.columns]

pg.rename(columns={'interceptions': 'ints'}, inplace=True)

# Missing data
pbp = pd.read_csv(path.join(DATA_DIR, 'play_data_sample.csv'))

pbp['yards_after_catch'].isnull().head()

pbp['yards_after_catch'].notnull().head()

pbp['yards_after_catch'].fillna(-99).head()

# Changing column types
pg['gameid'].head()

gameid = '2017090700'

year = gameid[0:4]
month = gameid[4:6]
day = gameid[6:8]

year
month
day

# pg['month'] = pg['gameid'].str[4:6]  # commented out since it gives an error

pg['month'] = pg['gameid'].astype(str).str[4:6]
pg[['month', 'gameid']].head()

pg['month'].astype(int).head()

pg.dtypes.head()

###########
# Exercises
###########

# 3.2.1
# ANS:
pg = pd.read_csv(path.join(DATA_DIR, 'player_game_2017_sample.csv'))
# TEST:
pg.head()
pg.columns

# 3.2.2
# ANS:
pg['rec_pts_ppr'] = 0.1 * pg['rec_yards'] + 6 * pg['rec_tds'] + 1 * pg['receptions']
# TEST:
pg.head()

# 3.2.3
# ANS:
pg['player_desc'] = pg['player_name'] + ' is the ' + pg['team'] + ' ' + pg['pos'] 
# TEST:
pg['player_desc']
pg.head()

# 3.2.4
# ANS:
pg['is_possession_rec'] = pg['caught_airyards'] > pg['raw_yac']
# TEST:
pg.sample(5)

# 3.2.5
# ANS:
pg['len_last_name'] = pg['player_name'].apply(lambda name: len(name.split('.')[-1]))
# TEST:
pg.head()

# 3.2.6
# ANS:
pg['gameid'] = pg['gameid'].astype(str)
# TEST:
pg.dtypes

# 3.2.7
# a)
pg.columns = [ col.replace('_', ' ') for col in pg.columns ]
# TEST:
pg.columns
# b)
pg.columns = [ col.replace(' ', '_') for col in pg.columns ]
# TEST
pg.columns

# 3.2.8
# a)
pg['rush_td_percentage'] = pg['rush_tds'] / pg['carries']
# TEST:
pg.sample(5)
pg['carries'].isnull().values.any()
# b)
# Since you are dividing by carries, which are often 0 for non-RBs, you get some missing values
pg['rush_td_percentage'] = pg['rush_td_percentage'].fillna(-99)
# TEST:
pg.sample(5)

# 3.2.9
# ANS:
pg = pg.drop('rush_td_percentage', axis = 1)
# TEST:
pg['rush_td_percentage']
pg.sample(5)
