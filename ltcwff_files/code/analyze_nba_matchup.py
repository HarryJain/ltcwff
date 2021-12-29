# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 19:14:22 2021

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

teams = {'ATL': 'Atlanta Hawks', 'BOS': 'Boston Celtics', 'BRK': 'Brooklyn Nets', 'CHO': 'Charlotte Hornets', 'CHI': 'Chicago Bulls', 'CLE': 'Cleveland Cavaliers', 'DAL': 'Dallas Mavericks', 'DEN': 'Denver Nuggets', 'DET': 'Detroit Pistons', 'GSW': 'Golden State Warriors', 'HOU': 'Houston Rockets', 'IND': 'Indiana Pacers', 'LAC': 'Los Angeles Clippers', 'LAL': 'Los Angeles Lakers', 'MEM': 'Memphis Grizzlies', 'MIA': 'Miami Heat', 'MIL': 'Milwaukee Bucks', 'MIN': 'Minnesota Timberwolves', 'NOP': 'New Orleans Pelicans', 'NYK': 'New York Knicks', 'OKC': 'Oklahoma City Thunder', 'ORL': 'Orlando Magic', 'PHI': 'Philadelphia 76ers', 'PHO': 'Phoenix Suns', 'POR': 'Portland Trail Blazers', 'SAC': 'Sacramento Kings', 'SAS': 'San Antonio Spurs', 'TOR': 'Toronto Raptors', 'UTA': 'Utah Jazz', 'WAS': 'Washington Wizards'}


def get_url_from_team(team, year, games = '', prefix = 'https://www.basketball-reference.com/teams'):
    return f'{prefix}/{team}/{year}{games}.html'


def get_soup(team, year, games = ''):
    url = get_url_from_team(team, year, games)
    print(url)
    response = requests.get(url)
    if not 200 <= response.status_code < 300:
        exit('Invalid Team')
    return Soup(response.content, 'html.parser')


def parse_row(row):
    result = [ x.string for x in row.find_all('td') ]
    return result


def table_to_df(table, overheader = 0):
    cols = table.find('thead').find_all('tr')[overheader].find_all('th')
    cols = [ col.string for col in cols ]
    cols
    
    stat_table = table.find('tbody')
    stat_table
        
    rows = stat_table.find_all('tr')
    rows
    
    headers = [ row.find('th').string for row in rows ]
    headers = [ header for header in headers if header != 'G' ]
    
    list_of_parsed_rows = [ parse_row(row) for row in rows[0:len(rows)] ]
    list_of_parsed_rows = [ row for row in list_of_parsed_rows if row != [] ]
    list_of_parsed_rows
    
    df = DataFrame(list_of_parsed_rows)
    df.insert(0, '', headers)
    df.columns = cols
    
    return df


def get_team_misc(soup, team, year):    
    div = soup.find('div', {'id': 'all_team_misc'})
    comment = div.find(string = lambda text: isinstance(text, Comment))
    table = Soup(comment, 'html.parser')
    table

    return table_to_df(table, 1)    


def get_team_stats(soup, team, year, prompt = 'Team to research: '):    
    divs = soup.find_all('div', {'id': 'all_team_and_opponent'})
    comments = divs[0].find_all(string = lambda text: isinstance(text, Comment))
    table = Soup(comments[0], 'html.parser')
    
    return table_to_df(table, 0)


def get_team_dfs(team, year = 2021):
    soup = get_soup(team, year)
    
    main_df = get_team_stats(soup, team, year)
    
    misc_df = get_team_misc(soup, team, year)
    
    return [main_df, misc_df]


def get_all_games(team, year = 2021):
    soup = get_soup(team, year, '_games')
    
    table = soup.find('table', {'id': 'games'})
    table
    
    tds = table.find_all('td', {'data-stat': 'box_score_text'})
    hrefs = [ f"https://www.basketball-reference.com{td.find('a')['href']}" for td in tds ]
        
    df = table_to_df(table)
    
    df['url'] = hrefs
    
    return df

def get_game_stats(url):
    response = requests.get(url)
    if not 200 <= response.status_code < 300:
        exit('Invalid Game')
    soup = Soup(response.content, 'html.parser')
    
    line_div = soup.find('div', {'id': 'all_line_score'})
    line_comment = line_div.find(string = lambda text: isinstance(text, Comment))
    line_table = Soup(line_comment, 'html.parser')
    
    factors_div = soup.find('div', {'id': 'all_four_factors'})
    factors_comment = factors_div.find(string = lambda text: isinstance(text, Comment))
    factors_table = Soup(factors_comment, 'html.parser')
    
    line_df = table_to_df(line_table, 1)
    line_df = line_df.set_index(line_df.columns[0])
    factors_df = table_to_df(factors_table, 1)
    factors_df = factors_df.set_index(factors_df.columns[0])
    
    df = pd.concat([line_df, factors_df], axis = 1)
    
    return df


def main():
    raw_odds_data = pd.read_csv(path.join(DATA_DIR, 'nba_odds_2020-21.csv'))
    
    odds_data = pd.DataFrame(columns = ['Away_Team', 'Away_1st', 'Away_2nd', 'Away_3rd', 'Away_4th', 'Home_Team', 'Home_1st', 'Home_2nd', 'Home_3rd', 'Home_4th'])
    #odds_data.columns = ['Away_Team', 'Away_1st', 'Away_2nd', 'Away_3rd', 'Away_4th', 'Home_Team', 'Home_1st', 'Home_2nd', 'Home_3rd', 'Home_4th']
    
    i = 0
    while i < len(raw_odds_data.index):
        row = {}
        row['Away_Team'] = raw_odds_data.loc[raw_odds_data.index[i], 'Team']
        row['Away_ML'] = raw_odds_data.loc[raw_odds_data.index[i], 'ML']
        row['Away_1st'] = raw_odds_data.loc[raw_odds_data.index[i], '1st']
        row['Away_2nd'] = raw_odds_data.loc[raw_odds_data.index[i], '2nd']
        row['Away_3rd'] = raw_odds_data.loc[raw_odds_data.index[i], '3rd']
        row['Away_4th'] = raw_odds_data.loc[raw_odds_data.index[i], '4th']
        row['Away_Final'] = raw_odds_data.loc[raw_odds_data.index[i], 'Final']
        row['Home_Team'] = raw_odds_data.loc[raw_odds_data.index[i + 1], 'Team']
        row['Home_ML'] = raw_odds_data.loc[raw_odds_data.index[i + 1], 'ML']
        row['Home_1st'] = raw_odds_data.loc[raw_odds_data.index[i + 1], '1st']
        row['Home_2nd'] = raw_odds_data.loc[raw_odds_data.index[i + 1], '2nd']
        row['Home_3rd'] = raw_odds_data.loc[raw_odds_data.index[i + 1], '3rd']
        row['Home_4th'] = raw_odds_data.loc[raw_odds_data.index[i + 1], '4th']
        row['Home_Final'] = raw_odds_data.loc[raw_odds_data.index[i + 1], 'Final']
        #print(row)
        odds_data = odds_data.append(row, ignore_index = True)
        i += 2
        
    print(odds_data)
    
    team_1 = input('Team 1: ')
    team_2 = input('Team 2: ')
    
    team_1_dfs = get_team_dfs(team_1)
    print(team_1_dfs[0])
    print(team_1_dfs[1])
    
    team_2_dfs = get_team_dfs(team_2)
    print(team_2_dfs[0])
    print(team_2_dfs[1])
    
    games = get_all_games(team_1)
    head_to_heads = [ games.loc[ind, :] for ind in games.index if games.loc[ind, 'Opponent'] == teams[team_2] ]
    #head_to_heads = games.loc[games['Opponent'] == teams[team_2], :]
    print(head_to_heads)
    
main()