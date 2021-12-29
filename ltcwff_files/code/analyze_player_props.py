# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 15:32:37 2021

@author: Harry
"""

# Module Imports
from bs4 import BeautifulSoup as Soup
from sys import exit
from os import path
import requests
import pandas as pd
from time import sleep
from datetime import date
from unidecode import unidecode


DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data\\player_props'


def get_url_from_player(player, prefix = 'https://www.basketball-reference.com/players'):
    first_name = player.split(' ')[0].lower()
    last_name = player.split(' ')[1].lower()
    num = 1
    return f'{prefix}/{last_name}[0]/{last_name[:5]}{first_name[:2]}{num:02d}.html'


def get_soup(player, year = '2021'):
    prefix = 'https://www.basketball-reference.com/players'
    first_name = player.split(' ')[0].lower()
    last_name = player.split(' ')[1].lower()
    num = 1
    
    while num != 0:
        url = f'{prefix}/{last_name[0]}/{last_name[:5]}{first_name[:2]}{num:02d}/gamelog/{year}'
        print(url)
        response = requests.get(url)
        if not 200 <= response.status_code < 300:
            exit('Invalid Date')
        else:
            soup = Soup(response.content, 'html.parser')
            num = 0
            #name = soup.find('h1', itemprop = 'name').find('span').string
            #name = unidecode(f"{name.split(' ')[0]} {name.split(' ')[1]}")
            #if name != player:
            #    num += 1
            #else:
            #    num = 0
    return soup


def parse_row(row):
    #result = [ x.string if x.find('a') == None else x.find('a').string for x in row.find_all('td') ]
    #return result
    result = [ x.string for x in row.find_all('td') ]
    #print(result)
    return result


def table_to_df(table, overheader = 0):
    cols = table.find('thead').find_all('tr')[overheader].find_all('th')
    cols = [ col.string if col.string != None else '' for col in cols[1:] ]
    #print(cols)
    
    stat_table = table.find('tbody')
        
    rows = stat_table.find_all('tr')
    
    #headers = [ row.find('th').string for row in rows if row.find('th') != None ]
    
    list_of_parsed_rows = [ parse_row(row) for row in rows[0:len(rows)] ]
    list_of_parsed_rows = [ row for row in list_of_parsed_rows if row != [] ]
    list_of_parsed_rows
    
    df = pd.DataFrame(list_of_parsed_rows)
    #if len(headers) != 0:
    #    df.insert(0, '', headers)
    df.columns = cols
    
    return df


def get_player_df(player):
    soup = get_soup(player)
    table = soup.find('table', id = 'pgl_basic')
    if table == None:
        return None
    df = table_to_df(table)
    
    df = df.dropna(axis = 0, subset = ['G'])
    
    df = df.drop(df.columns[0], axis = 1)
    df['Date'] = df['Date'].apply(lambda s: s.replace('-', ''))
    return df
    

today = date.today()
datef = today.strftime("%Y%m%d")
print(datef)
datef = '20210225'

props = pd.read_csv(path.join(DATA_DIR, f'{datef}.csv'))
props = props.drop(props.columns[0], axis = 1)
players = list(props['Player'].unique())
players

df = get_player_df(players[0])
df.columns
#print(type(df))

if not df is None:
    # Convert possible rows to numeric values
    for col in ['MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'GmSc', '+/-']:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            continue
        
    #print(df.columns)
                
    # Calculate means of team stats and add it to the combined DataFrame
    #means = df.iloc[[0, 1], :].mean()
    #means.name = 'Mean'
    #composite_df.append(means)

    df = df.append(df.mean(), ignore_index = True)
    print(df)

'''
for player in players:
    df = get_player_df(player)
    #print(type(df))
    
    if not df is None:
        # Convert possible rows to numeric values
        for col in ['TRB', 'AST', 'PTS']:
            try:
                df[col] = pd.to_numeric(df[col])
            except:
                continue
            
        #print(df.columns)
                    
        # Calculate means of team stats and add it to the combined DataFrame
        #means = df.iloc[[0, 1], :].mean()
        #means.name = 'Mean'
        #composite_df.append(means)
    
        df = df.append(df.mean(), ignore_index = True)
        print(df)
'''