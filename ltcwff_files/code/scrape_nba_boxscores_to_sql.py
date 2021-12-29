# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 19:40:57 2021

@author: Harry
"""

# Module Imports
from bs4 import BeautifulSoup as Soup
from sys import exit
from os import path
import requests
from pandas import DataFrame
import pandas as pd
from time import sleep
from datetime import date
import sqlite3


# Global Variables
DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'

team_dict = {'Atlanta': 'ATL', 'Boston': 'BOS', 'Brooklyn': 'BRK', 'Charlotte': 'CHO', 'Chicago': 'CHI', 'Cleveland': 'CLE', 'Dallas': 'DAL', 'Denver': 'DEN', 'Detroit': 'DET', 'Golden State': 'GSW', 'Houston': 'HOU', 'Indiana': 'IND', 'LA': 'LAC', 'L.A. Lakers': 'LAL', 'LA Lakers': 'LAL', 'LA Clippers': 'LAC', 'L.A. Clippers': 'LAC', 'Memphis': 'MEM', 'Miami': 'MIA', 'Milwaukee': 'MIL', 'Minnesota': 'MIN', 'New Orleans': 'NOP', 'New York': 'NYK', 'Oklahoma City': 'OKC', 'Orlando': 'ORL', 'Philadelphia': 'PHI', 'Phoenix': 'PHO', 'Portland': 'POR', 'Sacramento': 'SAC', 'San Antonio': 'SAS', 'Toronto': 'TOR', 'Utah': 'UTA', 'Washington': 'WAS'}


# Return the boxscore url for a given month, day, and year
def get_url_from_date(month, day, year, prefix = 'https://www.basketball-reference.com/boxscores'):
    return f'{prefix}/?month={month}&day={day}&year={year}'


# Return the soup for the boxscores for a given month, day, and year
def get_soup(month, day, year):
    url = get_url_from_date(month, day, year)
    print(url)
    response = requests.get(url)
    if not 200 <= response.status_code < 300:
        exit('Invalid Date')
    return Soup(response.content, 'html.parser')


# Return a list of elements in a table row
def parse_row(row):
    result = [ x.string if x.find('a') == None else x.find('a').string for x in row.find_all('td') ]
    return result


# Convert a web data table to a DataFrame, with an option to deal with an overheader
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


# Return a list of dictionaries including the game details for every game for a given month, day, and year
def get_all_games(month, day, year):
    soup = get_soup(month, day, year)

    boxscores = soup.find_all('div', {'class': 'game_summary expanded nohover'})

    if boxscores != None:
        tables = [ table_to_df(boxscore.find_all('table')[1]) for boxscore in boxscores ]

    rows = []

    i = 0
    for table in tables:
        row = {'Date': f'{year}{month:02}{day:02}', 'Home Team': table.iloc[1, 0], 'Away Team': table.iloc[0, 0], 'Home 1': int(table.iloc[1, 1]), 'Away 1': int(table.iloc[0, 1]), 'Home 2': int(table.iloc[1, 2]), 'Away 2': int(table.iloc[0, 2]), 'Home 3': int(table.iloc[1, 3]), 'Away 3': int(table.iloc[0, 3]), 'Home 4': int(table.iloc[1, 4]), 'Away 4': int(table.iloc[0, 4]), 'Home OT': int(table.iloc[1, 5]) if len(table.columns) >= 6 else 0, 'Away OT': int(table.iloc[0, 5]) if len(table.columns) >= 6 else 0, 'Home 2OT': int(table.iloc[1, 6]) if len(table.columns) >= 7 else 0, 'Away 2OT': int(table.iloc[0, 6]) if len(table.columns) >= 7 else 0, 'Home 3OT': int(table.iloc[1, 7]) if len(table.columns) >= 8 else 0, 'Away 3OT': int(table.iloc[0, 7]) if len(table.columns) >= 8 else 0}
        row['Home T'] = int(row['Home 1']) + int(row['Home 2']) + int(row['Home 3']) + int(row['Home 4']) + int(row['Home OT']) + int(row['Home 2OT']) + int(row['Home 3OT'])
        row['Away T'] = int(row['Away 1']) + int(row['Away 2']) + int(row['Away 3']) + int(row['Away 4']) + int(row['Away OT']) + int(row['Away 2OT']) + int(row['Away 3OT'])
        season = get_season({'year': year, 'month': month, 'day': day})
        row['Season'] = season[0]
        row['Playoffs'] = season[1]
        row['Link'] = boxscores[i].find('p').find_all('a')[0].get('href')
        rows.append(row)
        i += 1

    return rows


# Global variables for determining relevant dates to scrape
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

year = 2015
month = 10
day = 1

all_rows = []

toall = date.today()
toyear = toall.strftime("%Y")
toyear
tomonth = toall.strftime("%m")
tomonth
today = toall.strftime("%d")
today

season_dates = {
    '2015-16': {
        'start': {
            'year': 2015,
            'month': 10,
            'day': 27,
        },
        'regular': {
            'year': 2016,
            'month': 4,
            'day': 13,
        },
        'playoffs': {
            'year': 2016,
            'month': 6,
            'day': 19,
        },
    },
    '2016-17': {
        'start': {
            'year': 2016,
            'month': 10,
            'day': 25,
        },
        'regular': {
            'year': 2017,
            'month': 4,
            'day': 12,
        },
        'playoffs': {
            'year': 2017,
            'month': 6,
            'day': 12,
        },
    },
    '2017-18': {
        'start': {
            'year': 2017,
            'month': 10,
            'day': 17,
        },
        'regular': {
            'year': 2018,
            'month': 4,
            'day': 11,
        },
        'playoffs': {
            'year': 2018,
            'month': 6,
            'day': 8,
        },
    },
    '2018-19': {
        'start': {
            'year': 2018,
            'month': 10,
            'day': 16,
        },
        'regular': {
            'year': 2019,
            'month': 4,
            'day': 10,
        },
        'playoffs': {
            'year': 2019,
            'month': 6,
            'day': 13,
        },
    },
    '2019-20': {
        'start': {
            'year': 2019,
            'month': 10,
            'day': 22,
        },
        'regular': {
            'year': 2020,
            'month': 8,
            'day': 14,
        },
        'playoffs': {
            'year': 2020,
            'month': 10,
            'day': 11,
        },
    },
    '2020-21': {
        'start': {
            'year': 2020,
            'month': 12,
            'day': 22,
        },
        'regular': {
            'year': 2021,
            'month': 5,
            'day': 16,    
        },
        'playoffs': {
            'year': 2021,
            'month': tomonth,
            'day': today,
        },
    },
}

season_len = len(list(season_dates.keys()))


# Return whether the first dictionary of month, day, and year is after the second such dictionary
def is_after(date1_dict, date2_dict):
    if int(date1_dict['year']) > int(date2_dict['year']):
        return True
    elif int(date1_dict['year']) == int(date2_dict['year']):
        if int(date1_dict['month']) > int(date2_dict['month']):
            return True
        elif int(date1_dict['month']) == int(date2_dict['month']):
            if int(date1_dict['day']) > int(date2_dict['day']):
                return True
            else:
                return False       
        else:
            return False     
    else:
        return False
    
    
# Return a tuple (SEASON, IS_PLAYOFFS) given a date dictionary   
def get_season(date_dict):
    for i in range(season_len):
        season = list(season_dates.keys())[i]
        if not is_after(date_dict, season_dates[season]['regular']):
            return (season, False)
        elif not is_after(date_dict, season_dates[season]['playoffs']):
            return (season, True)
    return ('2020-21', True)


# Loop through all the relevant days and get the games for each
#for i in range(30):
while not (year == int(toyear) and month == int(tomonth) and day == int(today)):
    rows = get_all_games(month, day, year)
    #print(rows)
    all_rows = all_rows + rows
    
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


# Combine the rows of game data into one DataFrame, converting the link column to a game_id index and converting to team abbreviations
df = pd.DataFrame(all_rows)
df = df.set_index(df['Link'].apply(lambda link: link.split('/')[-1].split('.')[0]))
df.index.name = 'game_id'
df = df.drop('Link', axis = 1)
df['Home Team'] = df['Home Team'].apply(lambda team: team_dict[team])
df['Away Team'] = df['Away Team'].apply(lambda team: team_dict[team])
print(df)


# Write the games DataFrame to the database
conn = sqlite3.connect(path.join(DATA_DIR, 'nba.sqlite'))
df.to_sql('games', conn, if_exists = 'replace')


# Database test
teams = ('Detroit', 'Atlanta')
result = pd.read_sql(f'SELECT * FROM games WHERE "Home Team" IN {teams} AND "Away Team" IN {teams}', conn)
result


# Commit the database changes and close it
conn.commit()
conn.close()