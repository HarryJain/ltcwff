# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 14:48:56 2021

@author: Harry
"""

# Module Imports
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import pandas as pd
from time import sleep
from os import path
from datetime import date


# Global Variables
DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data\\player_props'

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


# Get all NBA games
url = 'https://sportsbook.fanduel.com/sports'

# Alternate URL/setup for NBA games directly
# url = 'https://sportsbook.fanduel.com/sports/navigation/830.1/10107.3'
# nba_index = 0

driver.get(url)
sleep(3)

marketplaces = driver.find_element_by_class_name('marketgroups').find_element_by_xpath("./*").find_elements_by_xpath("./*")

for i in range(len(marketplaces)):
    league = marketplaces[i].find_element_by_class_name('coupontitle').text
    if league == 'NBA':
        nba_index = i
        break

nba_games = marketplaces[nba_index].find_elements_by_class_name('event')
nba_games = [ game for game in nba_games if 'Today' in game.text ]
nba_games
        
game_ids = []
for game in nba_games:
    game_ids.append(game.find_element_by_xpath("./*").get_attribute('idfoevent'))
    
game_ids


# Get props for each game
all_filtered_dictionaries = []

for game_id in game_ids:
    #game_id = game_ids[0]
    url = f'https://sportsbook.fanduel.com/sports/event/{game_id}'
    print(url)
    driver.get(url)
    sleep(3)
    
    #all_buttons = driver.find_elements_by_class_name('tabs__item')
    #for button in all_buttons:
    #    print(button.text)
    #player_button = [ button for button in all_buttons if 'Player Props' in button.text ][0]
    
    prop_types = ['Points', 'Rebounds', 'Assists', 'Threes', 'Combos']
    
    filtered_props_lists = []
    
    for i in range(len(prop_types)):
        try:
            if i < 3:
                player_button = driver.find_element_by_xpath(f"//*[contains(text(), 'Player {prop_types[i]}')]")
                player_button.click()
            else:
                more_button = driver.find_element_by_xpath("//*[contains(text(), 'More')]")
                more_button.click()
                player_button = driver.find_element_by_xpath(f"//*[contains(text(), 'Player {prop_types[i]}')]")
                player_button.click()
            
            props = driver.find_elements_by_class_name('event-market-header')
            
            #for prop in props:
            #    print(prop.text)
            
            filtered_props = [ prop for prop in props if ' - ' in prop.text and 'Alt' not in prop.text ]
            
            #for prop in filtered_props:
            #    print(prop.text)
            
            for prop in filtered_props:
                prop.click()
                prop_list = prop.text.split('\n')
                if len(prop_list) == 9:
                    filtered_props_lists.append(prop_list)
                if len(prop.text.split('\n')) == 10 and 'same game parlay available' in prop.text.split('\n'):
                    prop_list.remove('same game parlay available')
                    filtered_props_lists.append(prop_list)
                #print(prop.text.split('\n'))
        except:
            continue
      
    filtered_props_lists
    
    filtered_props_dictionaries = [ {'Player': prop[0].split(' -')[0], 'Prop': prop[0].split('- ')[1], 'Over': float(prop[3]), 'Over Odds': int(prop[4]), 'Under': float(prop[7]), 'Under Odds': int(prop[8])} for prop in filtered_props_lists ]
    all_filtered_dictionaries = all_filtered_dictionaries + filtered_props_dictionaries
    print(pd.DataFrame(filtered_props_dictionaries))
    #points_df = pd.DataFrame(points_props_dictionaries)
    #print(points_df)

filtered_df = pd.DataFrame(all_filtered_dictionaries)
print(filtered_df)

today = date.today()
datef = today.strftime("%Y%m%d")
print(datef)

filtered_df.to_csv(path.join(DATA_DIR, f'{datef}.csv'))