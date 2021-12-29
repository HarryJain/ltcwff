import pandas as pd
import math
import statsmodels.formula.api as smf
from os import path

DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'

df = pd.read_csv(path.join(DATA_DIR, 'play_data_sample.csv'))
df = df.loc[(df['play_type'] == 'run') | (df['play_type'] == 'pass')]
df['offensive_td'] = ((df['touchdown'] == 1) & (df['yards_gained'] > 0))

model = smf.ols(formula=
        """
        wpa ~ offensive_td + turnover + first_down
        """, data=df)
results = model.fit()
results.summary2()

df.groupby('first_down')['yards_gained'].mean()

# adding yards_gained
model = smf.ols(formula=
        """
        wpa ~ offensive_td + turnover + first_down + yards_gained
        """, data=df)
results = model.fit()
results.summary2()

# fixed effects
pd.get_dummies(df['down']).head()
pd.get_dummies(df['down'], drop_first = True).head()

#############
# intractions
#############
df['turnover'] = df['turnover'].astype(int)
df['is_4'] = (df['qtr'] == 4).astype(int)

model = smf.ols(formula=
        """
        wpa ~ offensive_td + turnover + turnover:is_4 + yards_gained + first_down
        """, data=df)
results = model.fit()
results.summary2()

###########
# Exercises
###########

# 7.3
# a)
# ANS: throwing a pick is worse for a team's win probability because its coefficient is lower (-0.1850 vs -0.0560), which is almost definitely because fumbles can be recovered by the offense, while interceptions are always turnovers
model_a = smf.ols(data = df, formula = 'wpa ~ offensive_td + interception + yards_gained + fumble')
results_a = model_a.fit()
results_a.summary2()
results_a.params
# b)
# ANS: they are closer to each other, as I would expect, though there is still a significant difference which is tough to explain outside of small sample size
model_b = smf.ols(data = df, formula = 'wpa ~ offensive_td + interception + yards_gained + fumble_lost')
results_b = model_b.fit()
results_b.summary2()
results_b.params
