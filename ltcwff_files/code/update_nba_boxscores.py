# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 12:29:25 2021

@author: Harry
"""

from bs4 import BeautifulSoup as Soup
from bs4 import Comment
from sys import exit
from os import path
import requests
from pandas import DataFrame
import pandas as pd
from time import sleep
from datetime import date


DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'


def get_url_from_date(month, day, year, prefix = 'https://www.basketball-reference.com/boxscores'):
    return f'{prefix}/?month={month}&day={day}&year={year}'


def get_soup(month, day, year):
    url = get_url_from_date(month, day, year)
    print(url)
    response = requests.get(url)
    if not 200 <= response.status_code < 300:
        exit('Invalid Date')
    return Soup(response.content, 'html.parser')


def parse_row(row):
    result = [ x.string if x.find('a') == None else x.find('a').string for x in row.find_all('td') ]
    return result


def table_to_df(table, overheader = 0):
    cols = table.find('thead').find_all('tr')[overheader].find_all('th')
    cols = [ col.string if col.string != None else '' for col in cols ]
    
    stat_table = table.find('tbody')
        
    rows = stat_table.find_all('tr')
    
    headers = [ row.find('th').string for row in rows if row.find('th') != None ]
    
    list_of_parsed_rows = [ parse_row(row) for row in rows[0:len(rows)] ]
    list_of_parsed_rows = [ row for row in list_of_parsed_rows if row != [] ]
    list_of_parsed_rows
    
    df = DataFrame(list_of_parsed_rows)
    if len(headers) != 0:
        df.insert(0, '', headers)
    df.columns = cols
    
    return df


def get_all_games(month, day, year):
    soup = get_soup(month, day, year)

    boxscores = soup.find_all('div', {'class': 'game_summary expanded nohover'})

    if boxscores != None:
        tables = [ table_to_df(boxscore.find_all('table')[1]) for boxscore in boxscores ]

    rows = []

    for table in tables:
        row_1 = {'Date': f'{year}{month:02}{day:02}', 'Team': table.iloc[0, 0], '1': table.iloc[0, 1], '2': table.iloc[0, 2], '3': table.iloc[0, 3], '4': table.iloc[0, 4], 'T': int(table.iloc[0, 1]) + int(table.iloc[0, 2]) + int(table.iloc[0, 3]) + int(table.iloc[0, 4])}
        row_2 = {'Date': f'{year}{month:02}{day:02}', 'Team': table.iloc[1, 0], '1': table.iloc[1, 1], '2': table.iloc[1, 2], '3': table.iloc[1, 3], '4': table.iloc[1, 4], 'T': int(table.iloc[1, 1]) + int(table.iloc[1, 2]) + int(table.iloc[1, 3]) + int(table.iloc[1, 4])}
        rows.append(row_1)
        rows.append(row_2)

    return rows


days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

boxscores = pd.read_csv(path.join(DATA_DIR, 'scraped_nba_boxscores_2021.csv'))
boxscores = boxscores.drop(boxscores.columns[0], axis = 1)
boxscores
latest_date = str(boxscores.loc[boxscores.index[len(boxscores.index) - 1], 'Date'])

year = int(latest_date[0:4])
month = int(latest_date[4:6])
day = int(latest_date[6:8])

rows = boxscores.to_dict('records')

toall = date.today()
toyear = toall.strftime("%Y")
toyear
tomonth = toall.strftime("%m")
tomonth
today = toall.strftime("%d")
today

if day == days[month - 1]:
    day = 1
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
else:
    day += 1


#for i in range(4):
while not (year == int(toyear) and month == int(tomonth) and day == int(today)):
    daily_rows = get_all_games(month, day, year)
    
    rows = rows + daily_rows
    
    if day == days[month - 1]:
        day = 1
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
    else:
        day += 1
        

    sleep(1)

df = pd.DataFrame(rows)
print(df)

df.to_csv(path.join(DATA_DIR, 'scraped_nba_boxscores_2021.csv'))