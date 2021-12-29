# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 01:12:00 2021

@author: Harry
"""

import requests
from bs4 import BeautifulSoup as Soup

url = 'https://classic.sportsbookreview.com/betting-odds/nba-basketball/'

response = requests.get(url)

soup = Soup(response.content, 'html.parser')

print(soup.prettify())

all_games = soup.find('div', {'class': 'eventLines'})
all_games = all_games.find_all('div', {'class': 'event-holder holder-complete'})
all_games
spreads = all_games[0].find('div', {'class': 'el-div eventLine-book'}).find_all('div', {'class': 'eventLine-book-value'})
for spread in spreads:
    print(spread.string)