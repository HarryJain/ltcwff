import requests
from pandas import DataFrame
import pandas as pd

fc_url = 'https://fantasyfootballcalculator.com/api/v1/adp/ppr?teams=12&year=2017'

resp = requests.get(fc_url)
resp.json()

df = DataFrame(resp.json()['players'])
df.head()

def fc_adp(scoring='ppr', teams=12, year=2019):
    ffc_com = 'https://fantasyfootballcalculator.com'
    resp = requests.get(
        f'{ffc_com}/api/v1/adp/{scoring}?teams={teams}&year={year}'
    )
    df = DataFrame(resp.json()['players'])

    # data doesn't come with teams, year columns, let's add them
    df['year'] = year
    df['teams'] = teams
    return df

df_10_std = fc_adp('standard', 10, 2019)
df_10_std.head()
df_10_std[['name', 'adp']].head(10)

df_history = pd.concat(
    [fc_adp('standard', 12, year=y) for y in range(2009, 2020)],
    ignore_index=True)
df_history.head()
df_history.sample(5)

###########
# Exercises
###########

# 5.2.1
# ANS:
def get_response_table(year, export_type):
    url = f'https://api.myfantasyleague.com/{year}/export?TYPE={export_type}&JSON=1'
    response = requests.get(url)
    return DataFrame(response.json()[export_type]['player'])

def get_combined_200_table(year):
    adp_table = get_response_table(year, 'adp')
    players_table = get_response_table(year, 'players')
    combined = pd.merge(adp_table, players_table)
    return combined.loc[combined['position'].isin(['WR', 'RB', 'TE', 'QB', 'Def', 'PK'])].head(200)
# TEST:
get_combined_200_table(2019)[['name', 'position', 'averagePick']]
