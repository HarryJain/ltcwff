# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 17:00:40 2021

@author: Harry
"""

# Module Imports
from bs4 import BeautifulSoup as Soup
from bs4 import Comment
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

team_dict = {'San Francisco Giants': 'SFG', 'Los Angeles Dodgers': 'LAD', 'Chicago White Sox': 'CHW', 'Houston Astros': 'HOU', 'Boston Red Sox': 'BOS', 'Tampa Bay Rays': 'TBR', 'Milwaukee Brewers': 'MIL', 'Oakland Athletics': 'OAK', 'San Diego Padres': 'SDP', 'Seattle Mariners': 'SEA', 'New York Mets': 'NYM', 'Toronto Blue Jays': 'TOR', 'New York Yankees': 'NYY', 'Cincinnati Reds': 'CIN', 'Cleveland Indians': 'CLE', 'Philadelphia Phillies': 'PHI', 'St. Louis Cardinals': 'STL', 'Chicago Cubs': 'CHI', 'Atlanta Braves': 'ATL', 'Los Angeles Angels': 'LAA', 'Washington Nationals': 'WAS', 'Detroit Tigers': 'DET', 'Colorado Rockies': 'COL', 'Minnesota Twins': 'MIN', 'Miami Marlins': 'MIA', 'Kansas City Royals': 'KCR', 'Pittsburgh Pirates': 'PIT', 'Texas Rangers': 'TEX', 'Baltimore Orioles': 'BAL', 'Arizona Diamondbacks': 'ARI'}


# Return the boxscore url for a given month, day, and year
def get_url_from_date(month, day, year, prefix = 'https://www.baseball-reference.com/boxes'):
    return f'{prefix}/?year={year}&month={month}&day={day}'


# Return the soup for the boxscores for a given month, day, and year
def get_soup(month, day, year):
    url = get_url_from_date(month, day, year)
    print('\n')
    print(url)
    print()
    response = requests.get(url)
    if not 200 <= response.status_code < 300:
        exit('Invalid Date')
    return Soup(response.content, 'html.parser')


# Return a list of elements in a table row
def parse_row(row):
    result = [ x.string for x in row.find_all('td') ]
    return result


# Convert a web data table to a DataFrame, with an option to deal with an overheader
def table_to_df(table, overheader = 0, header = 'th'):
    cols = table.find('thead').find_all('tr')[overheader].find_all('th')
    cols = [ col.string if col.string != None else '' for col in cols ]
    
    stat_table = table.find('tbody')
        
    rows = stat_table.find_all('tr')
    
    headers = [ row.find(header).text for row in rows if row.find(header) != None ]
    
    list_of_parsed_rows = [ parse_row(row) for row in rows[0:len(rows)] ]
    list_of_parsed_rows = [ row for row in list_of_parsed_rows if row != [] ]
    list_of_parsed_rows
    
    df = DataFrame(list_of_parsed_rows)
    if len(headers) != 0:
        df.insert(0, '', headers)
    df.columns = cols
    
    return df


# Return a list of dictionaries including the game details for every game for a given month, day, and year
def get_all_links(month, day, year):
    soup = get_soup(month, day, year)

    boxscores = soup.find_all('div', {'class': 'game_summary nohover'})

    if boxscores != None:
        links = [ boxscore.find('td', {'class': 'right gamelink'}).find('a')['href'] for boxscore in boxscores ]
        links = [ link for link in links if 'allstar' not in link ]
        
    return links


# Return a list of dictionaries including the game details for every game for a given month, day, and year
def get_all_games(month, day, year):
    links = get_all_links(month, day, year)
    
    rows = []
    dfs = []
    
    for link in links:
        url = f'https://www.baseball-reference.com{link}'
        print(url)
        response = requests.get(url)
        soup = Soup(response.content, 'html.parser')
        
        '''
        OLD Pitchers
        pitcherTables = Soup(soup.find_all(text = lambda text:isinstance(text, Comment))[33], 'html.parser')
        awayPitchers = table_to_df(pitcherTables.find_all('table')[0])
        homePitchers = table_to_df(pitcherTables.find_all('table')[1])
        '''

        boxscore = soup.find('div', {'class': 'linescore_wrap'})
    
        if boxscore != None:
            footer = boxscore.find('tfoot').find('td').text.split('•')
            table = table_to_df(boxscore.find('table'))
            
            if not table.empty:
                # Get the pitcher tables from a comment
                pitcherTables = {}
                comments = soup.find_all(string = lambda text: isinstance(text, Comment))
                for comment in comments:
                    commentSoup = Soup(comment, 'html.parser')
                    awayPitchers = commentSoup.find('table', id = f'{"".join(table.iloc[0, 1].split(" ")).replace(".", "")}pitching')
                    if awayPitchers != None:
                        pitcherTables['away'] = table_to_df(awayPitchers, header = 'a')
                    homePitchers = commentSoup.find('table', id = f'{"".join(table.iloc[1, 1].split(" ")).replace(".", "")}pitching')
                    if homePitchers != None:
                        pitcherTables['home'] = table_to_df(homePitchers, header = 'a')
                    if 'away' in pitcherTables.keys() and 'home' in pitcherTables.keys():
                        break
            
                away = table.iloc[0, 2:]
                home = table.iloc[1, 2:]
                df = DataFrame([away, home])
                df.insert(0, 'game_id', link.split('/')[-1].split('.')[0])
                df.insert(0, 'Type', ['Away', 'Home'])
                df.insert(0, 'Team', [table.iloc[0, 1], table.iloc[1, 1]])
                #df['SP'] = [awayPitchers.iloc[0, 0], homePitchers.iloc[0, 0]]
                df['SP'] = [pitcherTables['away'].iloc[0, 0], pitcherTables['home'].iloc[0, 0]]
                df = df.set_index(['game_id', 'Type']).unstack()
                df.insert(0, 'Date', f'{year}{month:02}{day:02}')
                df['WP'] = footer[0].split("WP:")[1].split("(")[0].strip()
                df['WP Record'] = footer[0].split("WP:")[1].split("(")[1].strip()[:-1]
                df['LP'] = footer[1].split("LP:")[1].split("(")[0].strip()
                df['LP Record'] = footer[1].split("LP:")[1].split("(")[1].strip()[:-1]
                df['SV'] = footer[2].split("SV:")[1].split("(")[0].strip() if len(footer) > 2 else None
                df['SV Count'] = footer[2].split("SV:")[1].split("(")[1].strip()[:-1] if len(footer) > 2 else None
                #print(df)
                dfs.append(df)
                
                '''
                # Old version
                row = {'Date': f'{year}{month:02}{day:02}', 'Home Team': table.iloc[1, 1], 'Away Team': table.iloc[0, 1]}
                row['Link'] = link
                print(row)
                rows.append(row)
                '''
    
    if len(dfs) > 0:
        combined = pd.concat(dfs)
        combined.columns = [ f'{b} {a}' if b != '' else a for a, b in combined.columns ]
        return combined


# Global variables for determining relevant dates to scrape
season_dates = {
    '2020-21': {
        'start': {
            'year': 2021,
            'month': 4,
            'day': 1,
        },
        'regular': {
            'year': 2021,
            'month': 9,
            'day': 29,
        },
        'playoffs': {
            'year': 2021,
            'month': 11,
            'day': 15,
        },
    },
}

days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

year = season_dates['2020-21']['start']['year']
month = season_dates['2020-21']['start']['month']
day = season_dates['2020-21']['start']['day']

all_dfs = []

toall = date.today()
toyear = toall.strftime("%Y")
toyear
tomonth = toall.strftime("%m")
tomonth
today = toall.strftime("%d")
today

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
#for i in range(1):
while not (year == int(toyear) and month == int(tomonth) and day == int(today)):
    df = get_all_games(month, day, year)
    #print(rows)
    all_dfs.append(df)
    
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
big_df = pd.concat(all_dfs)
big_df['Home Team'] = big_df['Home Team'].apply(lambda team: team_dict[team])
big_df['Away Team'] = big_df['Away Team'].apply(lambda team: team_dict[team])
big_df = big_df.reindex(columns = ['Date', 'Away Team', 'Home Team', 'Away 1', 'Home 1', 'Away 2', 'Home 2', 'Away 3', 'Home 3', 'Away 4', 'Home 4', 'Away 5', 'Home 5', 'Away 6', 'Home 6', 'Away 7', 'Home 7', 'Away 8', 'Home 8', 'Away 9', 'Home 9', 'Away 10', 'Home 10', 'Away 11', 'Home 11', 'Away 12', 'Home 12', 'Away 13', 'Home 13', 'Away R', 'Home R', 'Away H', 'Home H', 'Away E', 'Home E', 'Away SP', 'Home SP', 'WP', 'WP Record', 'LP', 'LP Record', 'SV', 'SV Count'])
print(big_df)
big_df.iloc[0, :]

# Write the games DataFrame to the database
conn = sqlite3.connect(path.join(DATA_DIR, 'mlb.sqlite'))
big_df.to_sql('games', conn, if_exists = 'replace')


# Commit the database changes and close it
conn.commit()
conn.close()
