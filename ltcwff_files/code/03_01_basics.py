import pandas as pd
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'

##############
# Loading data
##############
adp = pd.read_csv(path.join(DATA_DIR, 'adp_2017.csv'))  # adp data

type(adp)

##################################
# DataFrame methods and attributes
##################################
adp.head()

adp.columns

adp.shape

#################################
# Working with subsets of columns
#################################
# A single column
adp['name'].head()

type(adp['name'])

adp['name'].to_frame().head()
type(adp['name'].to_frame().head())

# Multiple columns
adp[['name', 'position', 'adp']].head()

type(adp[['name', 'position', 'adp']])

# adp['name', 'position', 'adp'].head()  # commented out because it throws an error

##########
# Indexing
##########
adp[['name', 'position', 'adp']].head()

adp.set_index('player_id').head()

# Copies and the inplace argument
adp.head()  # note: player_id not the index, even though we just set it

adp.set_index('player_id', inplace=True)
adp.head()  # now player_id is index

# alternate to using inplace, reassign adp
adp = pd.read_csv(path.join(DATA_DIR, 'adp_2017.csv'))  # adp data
adp = adp.set_index('player_id')

adp.reset_index().head()

#############################
# Indexes keep things aligned
#############################
adp_rbs = adp.loc[adp['position'] == 'RB', ['name', 'position', 'team']]
adp_rbs.head()

adp_rbs.sort_values('name', inplace=True)
adp_rbs.head()

# assigning a new column
adp_rbs['adp'] = adp['adp']
adp_rbs.head()

# has the same index as adp_rbs and adp['adp']
adp['adp'].head()

#################
# Outputting data
#################
adp_rbs.to_csv(path.join(DATA_DIR, 'adp_rb.csv'))

adp_rbs.to_csv(path.join(DATA_DIR, 'adp_rb_no_index.csv'), index=False)

###########
# Exercises
###########

# 3.0.1
# ANS:
adp = pd.read_csv(path.join(DATA_DIR, 'adp_2017.csv'))
# ANS2:
adp = pd.read_csv(path.join(DATA_DIR, 'adp_2017.csv'))
# TEST:
adp.head()

# 3.0.1
# ANS:
adp50 = adp.sort_values('adp').head(50)
# ANS2:
adp50 = adp.sort_values('adp').head(50)    
# TEST:
adp50.head()
adp50.shape

# 3.0.3
# ANS:
adp.sort_values('name', ascending = False, inplace = True)
# ANS2:
adp = adp.sort_values('name', ascending = False)
# TEST:
adp.head()
adp['name'].head()

# 3.0.4
# ANS: DataFrame
# ANS2: DataFrame
# TEST:
type(adp.sort_values('adp'))

# 3.0.5
# ANS:
# a)
adp_simple = adp[['name', 'position', 'adp']]
# a2)
adp_simple = adp[['name', 'position', 'adp']]
# TEST:
adp_simple
# b)
adp_simple = adp_simple[['position', 'name', 'adp']]
# b2)
adp_simple = adp[['position', 'name', 'adp']].copy()
# TEST:
adp_simple
# c)
adp_simple['team'] = adp['team']
# c2)
adp_simple['team'] = adp['team']
adp_simple.loc[:, 'team'] = adp.loc[:, 'team']
# TEST:
adp_simple
# d)
adp_simple.to_csv(path.join(DATA_DIR, 'adp_simple.txt'), sep='|')
# d2)
adp_simple.to_csv(path.join(DATA_DIR, 'adp_simple.txt'), sep = '|')
