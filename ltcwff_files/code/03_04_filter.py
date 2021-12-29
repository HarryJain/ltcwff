import pandas as pd
import numpy as np
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'

adp = pd.read_csv(path.join(DATA_DIR, 'adp_2017.csv'))
adp.set_index('player_id', inplace=True)

# Filtering

tom_brady_id = 119
adp.loc[tom_brady_id]

my_player_ids = [119, 1886, 925]

adp.loc[my_player_ids]
adp.loc[my_player_ids, ['name', 'adp', 'stdev']]
adp.loc[my_player_ids, 'name']

# Boolean indexing
is_a_rb = adp['position'] == 'RB'

is_a_rb.head()

adp_rbs = adp.loc[is_a_rb]

adp_rbs[['name', 'adp', 'position']].head()
adp_df_wrs = adp.loc[adp['position'] == 'WR']

adp_df_wrs[['name', 'adp', 'position']].head()

is_a_te = adp['position'] == 'TE'

adp_not_te = adp.loc[~is_a_te]

adp_not_te[['name', 'adp', 'position']].head()

# Duplicates
adp.shape
adp.drop_duplicates(inplace=True)
adp.shape

adp.drop_duplicates('position')[['name', 'adp', 'position']]

adp.duplicated().head()

adp['position'].duplicated().head()
adp.duplicated('position').head()

adp.drop_duplicates('position')
adp.loc[~adp['position'].duplicated()]

# Combining filtering with changing columns
pg = pd.read_csv(path.join(DATA_DIR, 'player_game_2017_sample.csv'))

pg['primary_yards'] = np.nan
pg.loc[pg['pos'] == 'QB', 'primary_yards'] = pg['pass_yards']
pg.loc[pg['pos'] == 'RB', 'primary_yards'] = pg['rush_yards']
pg.loc[pg['pos'] == 'WR', 'primary_yards'] = pg['rec_yards']

pg[['player_name', 'pos', 'pass_yards', 'rush_yards', 'rec_yards', 'primary_yards']].sample(5)

# Added as a test by Harry
pg['total_yards'] = pg['pass_yards'] + pg['rush_yards'] + pg['rec_yards']
pg[['player_name', 'pos', 'pass_yards', 'rush_yards', 'rec_yards', 'primary_yards', 'total_yards']].sample(5)

# Query
pg.query("pos == 'RB'").head()

pg['is_a_rb'] = pg['pos'] == 'RB'

pg.query("is_a_rb").head()

# error: see below
#pg.query("raw_yac.notnull()")[['gameid', 'player_id', 'raw_yac']].head()

# note: if getting an error on line above, try it with engine='python' like
# this
pg.query("raw_yac.notnull()", engine='python')[['gameid', 'player_id', 'raw_yac']].head()

###########
# Exercises
###########

# 3.3.1
# ANS:
adp = pd.read_csv(path.join(DATA_DIR, 'adp_2017.csv'))
# ANS2:
adp = pd.read_csv(path.join(DATA_DIR, 'adp_2017.csv'))
# TEST:
adp.head()

# 3.3.2
# ANS:
# loc syntax
adp_cb1 = adp.loc[adp['team'] == 'DAL'][['name', 'position', 'adp']]
# TEST:
adp_cb1.head()
# Solution:
adp_cb1_solution = adp.loc[adp['team'] == 'DAL', ['name', 'position', 'adp']]
adp_cb1_solution
# query syntax
adp_cb2 = adp.query("team == 'DAL'")[['name', 'position', 'adp']]
adp_cb2.head()
# ANS2:
# loc syntax
adp_cb1 = adp.loc[adp['team'] == 'DAL', ['name', 'position', 'adp']]
# TEST:
adp_cb1.sample(5)
# query syntax
adp_cb2 = adp.query('team == "DAL"')[['name', 'position', 'adp']]
# TEST:
adp_cb2.sample(5)

# 3.3.3
# ANS:
# loc synatax
adp_no_cb1 = adp.loc[adp['team'] != 'DAL', ['name', 'position', 'adp', 'team']]
# TEST:
adp_no_cb1
# query syntax
adp_no_cb2 = adp.query("~(team == 'DAL')")[['name', 'position', 'adp', 'team']]
# TEST:
adp_no_cb2
# ANS2:
# loc syntax
adp_no_cb1 = adp.loc[adp['team'] != 'DAL', ['name', 'position', 'adp', 'team']]
# TEST:
adp_no_cb1.sample(5)
# query syntax
adp_no_cb2 = adp.query('team != "DAL"')[['name', 'position', 'adp', 'team']]
# TEST:
adp_no_cb2.sample(5)

# 3.3.4
# a)
# ANS: Yes, 23 (paris of) duplicates
adp['last_name'] = adp['name'].apply(lambda x: x.split(' ')[-1])
adp[['last_name', 'position']].duplicated().any()
np.count_nonzero(adp[['last_name', 'position']].duplicated())
# ANS2: Yes, 23 pairs of duplicates
adp['last_name'] = adp['name'].apply(lambda x: x.split(' ')[-1])
adp.duplicated(subset = ['last_name', 'position']).any()
adp.duplicated(subset = ['last_name', 'position']).sum()
# TEST:
np.count_nonzero(adp[['last_name', 'position']].query("last_name == 'Brown'").duplicated())
# b)
# ANS:
adp_dups = adp.loc[adp[['last_name', 'position']].duplicated(keep = False)]
adp_nodups = adp.loc[~adp[['last_name', 'position']].duplicated(keep = False)]
# ANS2:
adp_dups = adp.loc[adp.duplicated(subset = ['last_name', 'position'], keep = False)]
adp_nodups = adp.loc[~adp.duplicated(subset = ['last_name', 'position'], keep = False)]
# TEST:
adp_dups.duplicated(subset = ['last_name', 'position']).sum()
adp_nodups.duplicated(subset = ['last_name', 'position']).sum()
# Solution:
dups = adp[['last_name', 'position']].duplicated(keep = False)
adp_dups_sol = adp.loc[dups]
adp_nodups_sol = adp.loc[~dups]

# 3.3.5
# ANS:
adp['adp_description'] = np.nan
adp.loc[adp['adp'] < 40, 'adp_description'] = 'stud'
adp.loc[adp['adp'] > 120, 'adp_description'] = 'scrub'
# ANS2:
adp['adp_description'] = adp['adp'].apply(lambda x: 'stud' if x < 40 else 'scrub' if x > 120 else np.nan)
# TEST:
adp[['name', 'adp', 'adp_description']].sample(5)
adp[['name', 'adp', 'adp_description']].head()

# 3.3.6
# ANS:
# a) loc syntax
adp_no_desc1 = adp.loc[adp['adp_description'].isna()]
# a2) loc syntax
adp_no_desc1 = adp.loc[adp['adp_description'].isnull()]
# b) query syntax
adp_no_desc2 = adp.query('adp_description.isnull()', engine = 'python')
# b2) query syntax
adp_no_desc2 = adp.query("adp_description.isnull()", engine = 'python')
# TEST:
adp_no_desc1.head()
adp_no_desc2.head()
