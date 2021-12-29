import pandas as pd
import statsmodels.formula.api as smf
from os import path

DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'

###################
# linear regression
###################

# load
df = pd.read_csv(path.join(DATA_DIR, 'play_data_sample.csv'))

# process
df = df.loc[(df['play_type'] == 'run') | (df['play_type'] == 'pass')]
df['offensive_td'] = ((df['touchdown'] == 1) & (df['yards_gained'] > 0))
df['offensive_td'] = df['offensive_td'].astype(int)
df['yardline_100_sq'] = df['yardline_100'] ** 2

df[['offensive_td', 'yardline_100', 'yardline_100_sq']].head()

# run regression
model = smf.ols(formula='offensive_td ~ yardline_100 + yardline_100_sq', data=df)
results = model.fit()

results.summary2()
results.params

def prob_of_td(yds):
    b0, b1, b2 = results.params
    return (b0 + b1*yds + b2*(yds**2))

# Actually way too high for really far away
prob_of_td(75)
# Minimizes at 59.3457...ish cause mafs
prob_of_td(59)
prob_of_td(50)
prob_of_td(25)
prob_of_td(5)
prob_of_td(1)

df['offensive_td_hat'] = results.predict(df)
df[['offensive_td', 'offensive_td_hat']].head()

###########
# Exercises
###########

# 7.1
# a)
df['offensive_td_hat_alt'] = df['yardline_100'].apply(prob_of_td)
df[['offensive_td', 'offensive_td_hat', 'offensive_td_hat_alt']].head()
(results.predict(df) == df['offensive_td_hat_alt']).all()
# b)
# ANS: p value is 0.8304 so it is not significant
model_y = smf.ols(data = df, formula = 'offensive_td ~ yardline_100 + yardline_100_sq + ydstogo')
results_y = model_y.fit()
results_y.summary2()
results_y.params
# c)
# ANS: wrapping a variable in C() makes it a categorical variable and adds it to the model via fixed effects; 3rd down if most likely to lead to a touchdown due to highest coefficient (1st down is 0 since it is left off)
model_c = smf.ols(data = df, formula = 'offensive_td ~ yardline_100 + yardline_100_sq + C(down)')
results_c = model_c.fit()
results_c.summary2()
results_c.params
# d)
# ANS: yes, they are the same
dummies_df = pd.get_dummies(df['down'], drop_first = True)
dummies_df.columns = ['down_2', 'down_3', 'down_4']
df_d = pd.concat([df, dummies_df], axis = 1)
df_d.head()
model_d = smf.ols(data = df_d, formula = 'offensive_td ~ yardline_100 + yardline_100_sq + down_2 + down_3 + down_4')
results_d = model_d.fit()
results_d.summary2()
results_d.params
