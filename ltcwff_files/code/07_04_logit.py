import pandas as pd
import math
import statsmodels.formula.api as smf
from os import path

DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'

#####################
# logistic regression
#####################

# load
df = pd.read_csv(path.join(DATA_DIR, 'play_data_sample.csv'))

# process
df = df.loc[(df['play_type'] == 'run') | (df['play_type'] == 'pass')]
df['offensive_td'] = ((df['touchdown'] == 1) & (df['yards_gained'] > 0))
df['offensive_td'] = df['offensive_td'].astype(int)
df['yardline_100_sq'] = df['yardline_100'] ** 2

# run regression
model = smf.logit(formula='offensive_td ~ yardline_100 + yardline_100_sq',
                  data=df)
results = model.fit()
results.summary2()

def prob_of_td(yds):
    b0, b1, b2 = results.params
    value = (b0 + b1*yds + b2*(yds**2))
    return 1/(1 + math.exp(-value))

prob_of_td(75)
# Seems to plateau in the middle
# Minimizes at 60 from graph
prob_of_td(60)
prob_of_td(50)
prob_of_td(25)
prob_of_td(5)

###########
# Exercises
###########

# 7.4
# ANS: If my fellow fantasy players are very intelligent and skilled, I would expect them to account properly for the effect of rookies, which would make b2 very insignificant (close to 0); if they have inefficient biases/strategies, they might undervalue (b2 > 0) or overvalue (b2 < 0) rookies.
