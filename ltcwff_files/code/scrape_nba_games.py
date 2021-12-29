# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 01:09:58 2021

@author: Harry
"""

from bs4 import BeautifulSoup as Soup
from bs4 import Comment
from sys import exit
#from os import path
import requests
from pandas import DataFrame
import pandas as pd


DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'


def get_url_from_team(team, year, prefix = 'https://www.basketball-reference.com/teams'):
    return f'{prefix}/{team}/{year}_games.html'


def get_soup(team, year):
    url = get_url_from_team(team, year)
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

def get_all_games(team, year):
    soup = get_soup(team, year)
    
    table = soup.find('table', {'id': 'games'})
    table
    
    tds = table.find_all('td', {'data-stat': 'box_score_text'})
    hrefs = [ f"https://www.basketball-reference.com{td.find('a')['href']}" for td in tds ]
    
    #print(hrefs)
    
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

games = get_all_games('BOS', 2019)
print(games)
get_game_stats(games.loc[1, 'url'])
