# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 12:57:10 2021

@author: Harry
"""

from bs4 import BeautifulSoup as Soup
import requests
from pandas import DataFrame
import pandas as pd

def getUrlFromPlayer(player, num, prefix = 'https://www.pro-football-reference.com/players'):
    [first, last] = player.split(' ')
    return f'{prefix}/{last[0].upper()}/{last[0].upper()}{last[1:4]}{first[0:2]}{num}.htm'

def getSoup(player):
    num = 0
    status = 0
    repeat = True
    while repeat or not 200 <= status < 300:
        url = getUrlFromPlayer(player, num = f'{num:02d}')
        response = requests.get(url)
        status = response.status_code
        soup = Soup(response.content, 'html.parser')
        print(url)
        name_header = soup.find('h1', itemprop = 'name')
        name = name_header.find('span').string
        print(name)
        if "".join(name.split()) == "".join(player.split()):
            repeat = False
        num += 1
    return soup
    
def parse_row(row):
    result = [ str(x.string) for x in row.find_all('td') ]
    # Remove @ column
    #result.pop(2)
    return result

player = input('Player to research: ')

#print(player)

#url = getUrlFromPlayer(player)

#print(url)

#response = requests.get(url)
    
#print(response.status_code)
#print(nba_response.content)

soup = getSoup(player)


tables = soup.find_all('table')
len(tables)

stat_table = tables[0]
stat_table

rows = stat_table.find_all('tr')

headers = [ str(x.string) for x in rows[1].find_all('th') ]
headers = headers[1:len(headers)]
# Remove @ column
#headers.pop(2)

first_data_row = rows[2]

first_data_row.find_all('td')

list_of_parsed_rows = [ parse_row(row) for row in rows[2:len(rows) - 3] ]

df = DataFrame(list_of_parsed_rows)
#df.set_index(0, inplace=True)
df.columns = headers

for col in df.columns:
    try:
        df[col] = pd.to_numeric(df[col])
    except:
        #numeric_headers.remove(col)
        continue

print(df)
print(df.mean().round(2))

'''
# Parse out true numeric headers
numeric_headers = headers

for col in df.columns:
    try:
        df[col] = pd.to_numeric(df[col])
    except:
        numeric_headers.remove(col)
        continue

print(numeric_headers)
'''

#df[0:2]['Tgt']
#print(df.iloc[:, 9:14])