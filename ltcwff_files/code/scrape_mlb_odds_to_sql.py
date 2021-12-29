# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 18:31:29 2021

@author: Harry
"""


# Module Imports
import requests
from bs4 import BeautifulSoup as Soup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import pandas as pd
from pandas import DataFrame
from time import sleep
from os import path
from datetime import date, timedelta
import sqlite3


# Global Variables
DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'

team_dict = {'San Francisco Giants': 'SFG', 'Los Angeles Dodgers': 'LAD', 'Chicago White Sox': 'CHW', 'Houston Astros': 'HOU', 'Boston Red Sox': 'BOS', 'Tampa Bay Rays': 'TBR', 'Milwaukee Brewers': 'MIL', 'Oakland Athletics': 'OAK', 'San Diego Padres': 'SDP', 'Seattle Mariners': 'SEA', 'New York Mets': 'NYM', 'Toronto Blue Jays': 'TOR', 'New York Yankees': 'NYY', 'Cincinnati Reds': 'CIN', 'Cleveland Indians': 'CLE', 'Philadelphia Phillies': 'PHI', 'St. Louis Cardinals': 'STL', 'Chicago Cubs': 'CHI', 'Atlanta Braves': 'ATL', 'Los Angeles Angels': 'LAA', 'Washington Nationals': 'WAS', 'Detroit Tigers': 'DET', 'Colorado Rockies': 'COL', 'Minnesota Twins': 'MIN', 'Miami Marlins': 'MIA', 'Kansas City Royals': 'KCR', 'Pittsburgh Pirates': 'PIT', 'Texas Rangers': 'TEX', 'Baltimore Orioles': 'BAL', 'Arizona Diamondbacks': 'ARI'}
alt_team_dict = {'SFG': 'SFN', 'LAD': 'LAN', 'CHW': 'CHA', 'HOU': 'HOU', 'BOS': 'BOS', 'TBR': 'TBA', 'MIL': 'MIL', 'OAK': 'OAK', 'SDP': 'SDN', 'SEA': 'SEA', 'NYM': 'NYN', 'TOR': 'TOR', 'NYY': 'NYA', 'CIN': 'CIN', 'CLE': 'CLE', 'PHI': 'PHI', 'STL': 'SLN', 'CHI': 'CHN', 'ATL': 'ATL', 'LAA': 'ANA', 'WAS': 'WAS', 'DET': 'DET', 'COL': 'COL', 'MIN': 'MIN', 'MIA': 'MIA', 'KCR': 'KCA', 'PIT': 'PIT', 'TEX': 'TEX', 'BAL': 'BAL', 'ARI': 'ARI'}

headers = {
    'Host': 'www.amazon.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'TE': 'Trailers'
}

binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe') # this must point to where Firefox is installed on your machine
options = webdriver.FirefoxOptions() # this saves all the configuration settings for our webdriver
options.add_argument('-headless') # this will open the browser silently, not displaying a window
driver = webdriver.Firefox(firefox_binary = binary, executable_path = r'C:\\Program Files\\geckodriver-v0.29.0-win64\\geckodriver.exe', options = options)


# Get the date formatted according to my standard
today = date.today()
datef = today.strftime("%Y%m%d")


# Get a list of MLB game_ids on Baseball Reference for today
url = f'https://www.baseball-reference.com/boxes/?year={datef[:4]}&month={datef[4:6]}&day={datef[6:]}'
url = 'https://www.baseball-reference.com/previews/'

response = requests.get(url)
if not 200 <= response.status_code < 300:
    exit('Invalid Date')

soup = Soup(response.content, 'html.parser')

boxscores = soup.find_all('div', {'class': 'game_summary nohover'})

if boxscores != None:
    links = [ boxscore.find('td', {'class': 'right gamelink'}).find('a')['href'] for boxscore in boxscores if boxscore.find('td', {'class': 'right gamelink'}).find('a') != None ]
    game_ids = { link.split('/')[-1].split('.')[0]: False for link in links if 'allstar' not in link }
    print(game_ids)
    

# Get all MLB games on FanDuel
url = 'https://sportsbook.fanduel.com/navigation/mlb'

driver.get(url)
sleep(3)


# Get links to all the games that are not live
games = driver.find_elements_by_xpath('./html/body/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/*')
games = games[2: len(games) - 1]
games = [ game for game in games if 'INNING' not in game.text and game.text.split('\n')[-2][0].isdigit() ]
game_links = [ game.find_elements_by_xpath('./div/div/a') for game in games ]
game_links = [ game_link[0].get_attribute('href') for game_link in game_links if len(game_link) == 1 ]


# Loop through and create a row for each game
rows = []

for game_link in game_links[0:]:
    row = {}
    
    # Retry a few times for when the odds are live changing
    retry = 0
    while 0 <= retry <= 3:
        # Get basic game odds
        print(game_link)
        driver.get(game_link)
        sleep(3)
            
        # Turn the basic prop table into a list and create a row with the relevent components
        props = driver.find_elements_by_xpath('./html/body/div/div/div[2]/div/div/div[1]/div[2]/div[1]/div/div[2]/div[3]/div/div')
        basic = props[1].text
        basic_all = basic.split('\n')
        try:
            row = {'Away Team': team_dict[basic_all[4]], 'Home Team': team_dict[basic_all[6]], 'Away Spread': basic_all[8], 'Away Spread Odds': basic_all[9], 'Home Spread': basic_all[13], 'Home Spread Odds': basic_all[14], 'Away ML': basic_all[10], 'Home ML': basic_all[15], 'Over': basic_all[11].split(' ')[-1], 'Over Odds': basic_all[12], 'Under': basic_all[16].split(' ')[-1], 'Under Odds': basic_all[17]}    
        except:
            print(len(props))
            retry += 1
            continue
        
        # Get the corresponding Baseball Reference game_id and correct incorrect home/away teams
        row['game_id'] = [ game_id for game_id, used in game_ids.items() if (alt_team_dict[row['Home Team']] in game_id or alt_team_dict[row['Away Team']] in game_id) and used == False ][0]
        if alt_team_dict[row['Home Team']] not in row['game_id']:
            real_away = row['Home Team']
            row['Home Team'] = row['Away Team']
            row['Away Team'] = real_away
        
        # Get basic half game odds
        print(game_link + '?tab=1st-half')
        driver.get(game_link + '?tab=1st-half')
        sleep(3)
        
        props = driver.find_elements_by_xpath('./html/body/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[3]/div/div')    
        
        # If the expected half props are there, add them to the row
        if len(props) > 5 and '?tab=1st-half' in driver.current_url:    
            # Lists to index the props we want and the labels we apply to the split text list
            prop_indices = [1, 3, 4]
            prop_labels = [{3: 'Away 1H ML', 4: 'Home 1H ML'}, {2: 'Away 1H Spread', 3: 'Away 1H Spread Odds', 5: 'Home 1H Spread', 6: 'Home 1H Spread Odds'}, {4: '1H Over', 5: '1H Over Odds', 6: '1H Under', 7: '1H Under Odds'}]
            
            for i in range(len(prop_indices)):
                # Click button to expand prop if it is not the primary prop
                if i != 0:
                    try:
                        props[prop_indices[i]].click()
                    except:
                        continue
                # Get the data for the prop in a list and set the relevant row items
                prop_list = props[prop_indices[i]].text.split('\n')
                for index, label in prop_labels[i].items():
                    row[label] = prop_list[index]
        else:
            print(len(props))
            retry += 1
            continue
        
        # If it worked, stop retrying
        retry = -1
        
        
    # Add the row (empty or otherwise) to the DataFrame and mark the game_id as used (for double headers)
    game_ids[row['game_id']] = True
    rows.append(row)
    
    
# Combine the dataframes for each prop into a collective game dataframe and clean up the columns
df = DataFrame(rows)
if '1H Over' and '1H Under' in df.columns:
    df['1H Over'] = df['1H Over'].apply(lambda x: x.split(' ')[-1] if isinstance(x, str) else x)
    df['1H Under'] = df['1H Over'].apply(lambda x: x.split(' ')[-1] if isinstance(x, str) else x)
df.insert(0, 'Date', datef)
df = df.set_index('game_id')
df.iloc[:, 13:]
df[df.columns[3:]] = df[df.columns[3:]].apply(pd.to_numeric)
print(df)


# Combine the new odds rows with the pre-existing database table and write the combined DataFrame to the database
conn = sqlite3.connect(path.join(DATA_DIR, 'mlb.sqlite'))
try:
    old_df = pd.read_sql('SELECT * FROM odds', conn).set_index('game_id')
    new_df = pd.concat([old_df, df])
except:
    new_df = df
print(new_df)
new_df.to_sql('odds', conn, if_exists = 'replace')


# Commit the database changes and close it
conn.commit()
conn.close()
