# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 13:27:46 2021

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
url = 'https://sportsbook.fanduel.com/navigation/nba'

driver.get(url)
sleep(3)

# Old version
# games = driver.find_element_by_css_selector('div').find_element_by_css_selector('div').find_elements_by_xpath('./*')[1].find_elements_by_xpath('./*')[0].find_elements_by_xpath('./*')[0].find_elements_by_xpath('./*')[0].find_elements_by_xpath('./*')[1].find_elements_by_xpath('./*')[0].find_elements_by_xpath('./*')[0].find_elements_by_xpath('./*')[0].find_elements_by_xpath('./*')[0].find_elements_by_xpath('./*')[2].find_elements_by_xpath('./*')

# Slightly cleaner version - worked for MLB too so maybe robust?
games = driver.find_elements_by_xpath('./html/body/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/*')
games = games[2: len(games) - 1]
game_links = [ game.find_elements_by_xpath('./div/div/a') for game in games ]
game_links = [ game_link[0].get_attribute('href') for game_link in game_links if len(game_link) == 1 ]


# Loop through and create a dataframe for all the games
game_dfs = []

for game_link in game_links:
    '''
    OLD: didn't get all links
    if game.text == 'NBA Odds Boosts':
        break
    
    game_details = game.find_elements_by_xpath('./div/div/div')[0]
    more_details = game.find_elements_by_xpath('./div/div/a')[0]
    link = more_details.get_attribute('href')
    
    print(link)
    '''
    
    print(game_link)
    driver.get(game_link)
    sleep(3)
    
    driver.page_source
    buttons = driver.find_elements_by_xpath('./html/body/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div/div/div/div/div/nav/ul/li')
    
    prop_buttons = buttons[2:7]
    
    
    # Loop through and create a dataframe for all the prop buttons/types
    prop_dfs = []
    
    for prop_button in prop_buttons:
        # Get the relevant props for each tab
        prop_button.click()
        props = driver.find_elements_by_xpath('./html/body/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[3]/div/div')
        
        
        # Get prop values for each prop on the tab (need to generalize for combos)
        for i in range(1, 5 if prop_button.text == 'Player Combos' else 2):
            # Click button to expand prop if it is not the primary prop
            if i > 1:
                props[i].click()
            
            
            # Get list of player prop details for each player
            prop = props[i].find_elements_by_xpath('./div/div/div')
            prop_name = prop[0].text.replace('Player ', '')
            if prop[len(prop) - 1].text == 'Show more':
                prop[len(prop) - 1].click()
            
            players = prop[2].find_elements_by_xpath('./div')
            
            lists = [list((map(lambda string: string.replace('O ', '').replace('U ', ''), player.text.split('\n')))) for player in players]
            
            
            # Add dataframe for this prop to the list of prop dataframes
            df = pd.DataFrame(lists)
            df.insert(1, 'Prop', prop_name)
            df.columns = ['Player', 'Prop', 'Over', 'Over Odds', 'Under', 'Under Odds']
            df['Over Odds'] = df['Over Odds'].astype(int)
            df['Under Odds'] = df['Under Odds'].astype(int)
            prop_dfs.append(df)
    
    
    # Combine the dataframes for each prop into a collective game dataframe
    game_df = pd.concat(prop_dfs, ignore_index = True)
    #print(game_df)
    game_dfs.append(game_df)
    
    
# Combine the dataframes for each prop into a collective game dataframe and write to a csv
final_df = pd.concat(game_dfs, ignore_index = True)
print(final_df)

today = date.today()
datef = today.strftime("%Y%m%d")
print(datef)

final_df.to_csv(path.join(DATA_DIR, f'{datef}.csv'))