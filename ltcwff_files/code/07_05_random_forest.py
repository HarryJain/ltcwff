import pandas as pd
from pandas import DataFrame, Series
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from os import path

DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'

df = pd.read_csv(path.join(DATA_DIR, 'player_game_2017_sample.csv'))

train, test = train_test_split(df, test_size=0.20)

xvars = ['carries', 'rush_yards', 'rush_fumbles', 'rush_tds', 'targets',
         'receptions', 'rec_yards', 'raw_yac', 'rec_fumbles', 'rec_tds',
         'ac_tds', 'rec_raw_airyards', 'caught_airyards', 'attempts',
         'completions', 'pass_yards', 'pass_raw_airyards', 'comp_airyards',
         'timeshit', 'interceptions', 'pass_tds', 'air_tds']
yvar = 'pos'

train, test = train_test_split(df, test_size=0.20)
train, test

model = RandomForestClassifier(n_estimators=100)
model.fit(train[xvars], train[yvar])

test['pos_hat'] = model.predict(test[xvars])
test['correct'] = (test['pos_hat'] == test['pos'])
test['correct'].mean()

model.predict_proba(test[xvars])

probs = DataFrame(model.predict_proba(test[xvars]),
                  index=test.index,
                  columns=model.classes_)
probs.head()

results = pd.concat([
    test[['player_id', 'player_name', 'pos', 'pos_hat', 'correct']],
    probs], axis=1)
results
results.groupby('pos')[['correct', 'QB', 'RB', 'WR', 'TE']].mean()

# cross validation
model = RandomForestClassifier(n_estimators=100)
scores = cross_val_score(model, df[xvars], df[yvar], cv=10)

scores
scores.mean()

model.fit(df[xvars], df[yvar])

# feature importance
Series(model.feature_importances_, xvars).sort_values(ascending=False)

###########
# Exercises
###########

# 7.5
# a)
df_mean = df.groupby('player_id')[xvars].mean()
df_mean['pos'] = df.groupby('player_id')[yvar].first()
df_mean
model_mean = RandomForestClassifier(n_estimators = 100)
scores_mean = cross_val_score(model_mean, df_mean[xvars], df_mean[yvar], cv = 10)
scores_mean
scores_mean.mean()
# b)
df_med = df.groupby('player_id')[xvars].median()
df_med['pos'] = df.groupby('player_id')[yvar].first()
model_med = RandomForestClassifier(n_estimators = 100)
scores_med = cross_val_score(model_med, df_med[xvars], df_med[yvar], cv = 10)
scores_med
scores_med.mean()

df_max = df.groupby('player_id')[xvars].max()
df_max['pos'] = df.groupby('player_id')[yvar].first()
model_max = RandomForestClassifier(n_estimators = 100)
scores_max = cross_val_score(model_max, df_max[xvars], df_max[yvar], cv = 10)
scores_max
scores_max.mean()

df_min = df.groupby('player_id')[xvars].min()
df_min['pos'] = df.groupby('player_id')[yvar].first()
model_min = RandomForestClassifier(n_estimators = 100)
scores_min = cross_val_score(model_min, df_min[xvars], df_min[yvar], cv = 10)
scores_min
scores_min.mean()

df_mean = df.groupby('player_id')[xvars].mean()
df_med = df.groupby('player_id')[xvars].median()
df_max = df.groupby('player_id')[xvars].max()
df_min = df.groupby('player_id')[xvars].min()

df_mean.columns = [f'{x}_mean' for x in df_mean.columns]
df_med.columns = [f'{x}_med' for x in df_med.columns]
df_max.columns = [f'{x}_max' for x in df_max.columns]
df_min.columns = [f'{x}_min' for x in df_min.columns]

df_mult = pd.concat([df_mean, df_med, df_max, df_min], axis = 1)
df_mult

xvars_mult = list(df_mult.columns)

df_mult['pos'] = df.groupby('player_id')[yvar].first()

model_mult = RandomForestClassifier(n_estimators = 100)
scores_mult = cross_val_score(model_mult, df_mult[xvars_mult], df_mult[yvar], cv = 10)
scores_mult
scores_mult.mean()

