# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 22:27:08 2021

@author: Harry
"""

from bs4 import BeautifulSoup as Soup
from bs4 import Comment
from sys import exit
from os import path
import requests
from pandas import DataFrame
import pandas as pd


DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'


def get_url_from_player(team, year, prefix = 'https://www.basketball-reference.com/teams'):
    return f'{prefix}/{team}/{year}.html'


def get_soup(team, year):
    url = get_url_from_player(team, year)
    print(url)
    response = requests.get(url)
    if not 200 <= response.status_code < 300:
        exit('Invalid Team')
    return Soup(response.content, 'html.parser')

    
def parse_row(row):
    result = [ str(x.string) for x in row.find_all('td') ]
    # Remove @ column
    #result.pop(2)
    return result


def get_team_misc(soup, team, year):    
    div = soup.find('div', {'id': 'all_team_misc'})
    comment = div.find(string = lambda text: isinstance(text, Comment))
    table = Soup(comment, 'html.parser')
    table
    
    cols = table.find('thead').find_all('tr')[1].find_all('th')
    cols = [ col.string for col in cols ][1:17] + [ f'OPP {col.string}' for col in cols ][17:21] + [ col.string for col in cols ][21:]
    cols
    
    stat_table = table.find('tbody')
    
    rows = stat_table.find_all('tr')
    
    
    headers = [ row.find('th').string for row in rows ]
    headers
    
    list_of_parsed_rows = [ parse_row(row) for row in rows[0:len(rows)] ]
    #print(list_of_parsed_rows)
    df = DataFrame(list_of_parsed_rows)
    df
    df.insert(0, team, headers)
    #df.set_index('Category', inplace = True)
    df.columns = [ year ] + cols
    
    index = df.index
    index.name = team
    
    return df


def get_team_stats(soup, team, year, prompt = 'Team to research: '):
    #team = input(prompt)
    
    #soup = get_soup(team, year)
    #print(soup)
    
    
    divs = soup.find_all('div', {'id': 'all_team_and_opponent'})
    comments = divs[0].find_all(string = lambda text: isinstance(text, Comment))
    table = Soup(comments[0], 'html.parser')
    
    cols = table.find('thead').find_all('th')
    cols = [ col.string for col in cols ][1:]
    
    stat_table = table.find_all('tbody')[0]
    
    rows = stat_table.find_all('tr')
    
    
    headers = [ row.find_all('th')[0].string for row in rows ]
    headers
    
    list_of_parsed_rows = [ parse_row(row) for row in rows[0:len(rows)] ]
    #print(list_of_parsed_rows)
    df = DataFrame(list_of_parsed_rows)
    df.insert(0, team, headers)
    #df.set_index('Category', inplace = True)
    df.columns = [ year ] + cols
    
    index = df.index
    index.name = team
    
    return df


def get_team_dfs(team, year):
    soup = get_soup(team, year)
    
    main_df = get_team_stats(soup, team, year)
    
    misc_df = get_team_misc(soup, team, year)
    
    return [main_df, misc_df]


def convert_df_to_int(df):
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            continue
    return df


def team_df_to_dict(df, misc_df):
    team_misc = { f'{key}': misc_df.loc[1][key] for key in misc_df.columns[1:] }
    team_lg_misc = { f'LG {key}': misc_df.loc[2][key] for key in misc_df.columns[1:] }
    team = { f'{key}/G': df.loc[1][key] for key in df.columns[2:] }
    team_lg = { f'LG {key}/G': df.loc[2][key] for key in df.columns[2:] }
    opponent = { f'OPP {key}/G': df.loc[5][key] for key in df.columns[2:] }
    opponent_lg = { f'OPP LG {key}/G': df.loc[5][key] for key in df.columns[2:] }
    return {**team_misc, **team_lg_misc, **team, **team_lg, **opponent, **opponent_lg}


def team_df_to_list(df, misc_df):
    headers = [ df.index.name ] + [ df.columns[0] ]
    team_misc = [ misc_df.loc[0][key] for key in misc_df.columns[1:] ]
    team_misc_lg = [ misc_df.loc[1][key] for key in misc_df.columns[1:] ]
    team = [ df.loc[1][key] for key in df.columns[2:] ]
    team_lg = [ df.loc[2][key] for key in df.columns[2:] ]
    opponent = [ df.loc[5][key] for key in df.columns[2:] ]
    opponent_lg = [ df.loc[6][key] for key in df.columns[2:] ]
    return headers + team_misc + team_misc_lg + team + team_lg + opponent + opponent_lg


def main():
    teams = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
    years = ['2017', '2018', '2019', '2020', '2021']
    
    #df1 = convert_df_to_int(get_team_stats('Team 1: '))
    #print(df1)
    #df2 = convert_df_to_int(get_team_stats('Team 2: '))
    #print(df2)
    
    dfs = []
    misc_dfs = []
    
    for year in years:
        for team in teams:
            team_dfs = get_team_dfs(team, year)
            dfs.append(convert_df_to_int((team_dfs[0])))
            print(dfs[len(dfs) - 1])
            misc_dfs.append(convert_df_to_int((team_dfs[1])))
            print(misc_dfs[len(misc_dfs) - 1])
        
    lists = []
    
    for i in range(len(dfs)):
        lists.append(team_df_to_list(dfs[i], misc_dfs[i]))
    
    cols = [ 'Team' ] + [ 'Year' ] +  [ f'{col}' for col in misc_dfs[0].columns[1:] ] + [ f'LG {col}' for col in misc_dfs[0].columns[1:] ] + [ f'{col}/G' for col in dfs[0].columns[2:] ] + [ f'LG {col}/G' for col in dfs[0].columns[2:] ] + [ f'OPP {col}/G' for col in dfs[0].columns[2:] ] + [ f'LG OPP {col}/G' for col in dfs[0].columns[2:] ]

    #print(dfs)
    
    combined_df = pd.DataFrame(lists, columns = cols)
    combined_df.to_csv(path.join(DATA_DIR, 'team_data.csv'))
    print(combined_df)
    
main()

dfs = get_team_dfs('BOS', 2021)
dfs[1].iloc[:, 17:21]
