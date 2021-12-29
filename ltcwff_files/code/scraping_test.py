# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 01:08:41 2021

@author: Harry
"""

from bs4 import BeautifulSoup as Soup
import requests
from pandas import DataFrame

nba_response = requests.get('https://www.basketball-reference.com/leagues/NBA_2021_advanced.html')
#print(nba_response.content)

soup = Soup(nba_response.content, 'html.parser')
#print(soup.prettify())

tables = soup.find_all('table')

stat_table = tables[0]

rows = stat_table.find_all('tr')
first_data_row = rows[1]

first_data_row.find_all('td')

def parse_row(row):
    return [ str(x.string) for x in row.find_all('td') if x.string != None ]

list_of_parsed_rows = [parse_row(row) for row in rows[1:]]

df = DataFrame(list_of_parsed_rows)
df.set_index(0, inplace=True)
df