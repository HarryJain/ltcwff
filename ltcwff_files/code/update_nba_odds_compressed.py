# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 02:38:12 2021

@author: Harry
"""

# Module Imports
import pandas as pd
from os import path
from bs4 import BeautifulSoup as Soup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from time import sleep
from datetime import date

# Global Variables
DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'

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
driver = webdriver.Firefox(firefox_binary=binary, executable_path=r'C:\\Program Files\\geckodriver-v0.29.0-win64\\geckodriver.exe', firefox_options=options)


# Get Daily Odds Data
def get_daily_odds(current_date, period = '', period_formatted = ''):
    print(period)
    
    all_rows = []
    
    spread_url = f'https://classic.sportsbookreview.com/betting-odds/nba-basketball/{period}/?date={current_date}'

    driver.get(spread_url)
    
    spread_soup = Soup(driver.page_source, 'html.parser')

    
    all_game_spreads = spread_soup.find('div', {'class': 'eventLines'})
    if all_game_spreads == None:
        return
    #all_game_spreads
    all_game_spreads = all_game_spreads.find_all('div', {'class': 'event-holder holder-complete'})
    #all_game_spreads
    
    for game in all_game_spreads:
        row_1 = {}
        #row_2 = {}
    
        teams = [ x.string for x in game.find('div', {'class': 'el-div eventLine-team'}).find_all('a') ]
        book = 0
        spreads = None
        while spreads == None:
            try:
                spreads = [ x.string for x in game.find_all('div', {'class': 'el-div eventLine-book'})[book].find_all('div') ]
            except:
                break
            book += 1
        #print(teams)
        #print(spreads)
        
        row_1['Date'] = current_date
        #row_2['Date'] = current_date
        row_1['Home Team'] = teams[0]
        row_1['Away Team'] = teams[1]
        #row_2['Team'] = teams[1]
        
        if spreads[0] != None:
            #print(spreads)
            spread_1 = spreads[0].split('\xa0')
            #if len(spread_1) == 1 and spreads[0][0:2] == 'PK':
                #spread_1 = ['0', spreads[0][2:]]
            if spreads[0][0:2] == 'PK':
                spread_1[0] = '0'
                
            row_1[f'Home {period_formatted}Spread'] = float(spread_1[0]) if len(spread_1[0].split('½')) == 1 else float(f"{spread_1[0].split('½')[0]}.5")
            row_1[f'Home {period_formatted}Spread Odds'] = int(spread_1[1])
        else:
            row_1[f'Home {period_formatted}Spread'] = None
            row_1[f'Home {period_formatted}Spread Odds'] = None
            
        if spreads[1] != None:
            #print(spreads)
            spread_2 = spreads[1].split('\xa0')
            #if len(spread_2) == 1 and spreads[1][0:2] == 'PK':
                #spread_2 = ['0', spreads[1][2:]]
            if spreads[1][0:2] == 'PK':
                spread_2[0] = '0'
                
            #row_2[f'{period_formatted}Spread'] = float(spread_2[0]) if len(spread_2[0].split('½')) == 1 else float(f"{spread_2[0].split('½')[0]}.5")
            #row_2[f'{period_formatted}Spread Odds'] = int(spread_2[1])
            row_1[f'Away {period_formatted}Spread'] = float(spread_2[0]) if len(spread_2[0].split('½')) == 1 else float(f"{spread_2[0].split('½')[0]}.5")
            row_1[f'Away {period_formatted}Spread Odds'] = int(spread_2[1])
        else:
            #row_2[f'{period_formatted}Spread'] = None
            #row_2[f'{period_formatted}Spread Odds'] = None
            row_1[f'Away {period_formatted}Spread'] = None
            row_1[f'Away {period_formatted}Spread Odds'] = None
        
        all_rows.append(row_1)
        #all_rows.append(row_2)
        #print(row_1)
        #print(row_2)
        
    ml_url = f'https://classic.sportsbookreview.com/betting-odds/nba-basketball/money-line/{period}/?date={current_date}'

    driver.get(ml_url)
    
    ml_soup = Soup(driver.page_source, 'html.parser')
    
    all_game_mls = ml_soup.find('div', {'class': 'eventLines'})
    if all_game_mls == None:
        return
    
    all_game_mls = all_game_mls.find_all('div', {'class': 'event-holder holder-complete'})
    
    i = 0
    for game in all_game_mls:
        book = 0
        mls = None
        while mls == None or mls[0] == None or mls[1] == None:
            try:
                mls = [ x.string for x in game.find_all('div', {'class': 'el-div eventLine-book'})[book].find_all('b') ]
            except:
                break
            book += 1   
        #print(f'{mls[0]}, {mls[1]}')
        
        all_rows[i][f'Home {period_formatted}ML'] = int(mls[0]) if mls[0] != None else None
        all_rows[i][f'Away {period_formatted}ML'] = int(mls[1]) if mls[1] != None else None
        #all_rows[i + 1][f'{period_formatted}ML'] = int(mls[1]) if mls[1] != None else None
        
        i += 1
        
        
    total_url = f'https://classic.sportsbookreview.com/betting-odds/nba-basketball/totals/{period}/?date={current_date}'

    driver.get(total_url)
    
    total_soup = Soup(driver.page_source, 'html.parser')
    
    all_game_totals = total_soup.find('div', {'class': 'eventLines'})
    if all_game_totals == None:
        return
    
    all_game_totals = all_game_totals.find_all('div', {'class': 'event-holder holder-complete'})
    
    i = 0
    for game in all_game_totals:
        book = 0
        totals = None
        while totals == None:
            try:
                totals = [ x.string for x in game.find_all('div', {'class': 'el-div eventLine-book'})[book].find_all('b') ]
            except:
                book += 1
        #print(totals)
        
        if totals[0] != None:
            over = totals[0].split('\xa0')
            all_rows[i][f'{period_formatted}Over'] = float(over[0]) if len(over[0].split('½')) == 1 else float(f"{over[0].split('½')[0]}.5")
            #all_rows[i + 1][f'{period_formatted}Over'] = float(over[0]) if len(over[0].split('½')) == 1 else float(f"{over[0].split('½')[0]}.5")
            all_rows[i][f'{period_formatted}Over Odds'] = int(over[1])
            #all_rows[i + 1][f'{period_formatted}Over Odds'] = int(over[1])
        else:
            all_rows[i][f'{period_formatted}Over'] = None
            #all_rows[i + 1][f'{period_formatted}Over'] = None 
            all_rows[i][f'{period_formatted}Over Odds'] = None
            #all_rows[i + 1][f'{period_formatted}Over Odds'] = None
            
        if totals[1] != None:
            under = totals[1].split('\xa0')
            all_rows[i][f'{period_formatted}Under'] = float(under[0]) if len(under[0].split('½')) == 1 else float(f"{under[0].split('½')[0]}.5")
            #all_rows[i + 1][f'{period_formatted}Under'] = float(under[0]) if len(under[0].split('½')) == 1 else float(f"{under[0].split('½')[0]}.5")
            all_rows[i][f'{period_formatted}Under Odds'] = int(under[1])
            #all_rows[i + 1][f'{period_formatted}Under Odds'] = int(under[1])
        else:
            all_rows[i][f'{period_formatted}Under'] = None
            #all_rows[i + 1][f'{period_formatted}Under'] = None
            all_rows[i][f'{period_formatted}Under Odds'] = None
            #all_rows[i + 1][f'{period_formatted}Under Odds'] = None
        
        i += 1
        
        #print(row_1)
        #print(row_2)
        
    return all_rows


# Loop Through Data for All Days
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

odds = pd.read_csv(path.join(DATA_DIR, 'scraped_odds_data_2021_compressed.csv'))
odds = odds.drop(odds.columns[0], axis = 1)
odds
latest_date = str(odds.loc[odds.index[len(odds.index) - 1], 'Date'])

year = int(latest_date[0:4])
month = int(latest_date[4:6])
day = int(latest_date[6:8])

rows = odds.to_dict('records')

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
#while not (month == 5 and day == 31):
while not (year == int(toyear) and month == int(tomonth) and day == int(today)):
    current_date = f'{year}{month:02d}{day:02d}'
    print(f'\n\n{current_date}')
    odds = get_daily_odds(current_date)
    odds_1H = get_daily_odds(current_date, period = '1st-half', period_formatted = '1H ')
    odds_2H = get_daily_odds(current_date, period = '2nd-half', period_formatted = '2H ')
    odds_1Q = get_daily_odds(current_date, period = '1st-quarter', period_formatted = '1Q ')
    odds_2Q = get_daily_odds(current_date, period = '2nd-quarter', period_formatted = '2Q ')
    odds_3Q = get_daily_odds(current_date, period = '3rd-quarter', period_formatted = '3Q ')
    odds_4Q = get_daily_odds(current_date, period = '4th-quarter', period_formatted = '4Q ')
    #odds
    #odds_1H

    
    if odds != None:
        all_odds = []
        for i in range(len(odds)):
            all_odds.append({**odds[i], **odds_1H[i], **odds_2H[i], **odds_1Q[i], **odds_2Q[i], **odds_3Q[i], **odds_4Q[i]})
        #all_odds = [{**odds[0], **odds_1H[0], **odds_2H[0], **odds_1Q[0], **odds_2Q[0], **odds_3Q[0], **odds_4Q[0]}, {**odds[1], **odds_1H[1], **odds_2H[1], **odds_1Q[1], **odds_2Q[1], **odds_3Q[1], **odds_4Q[1]}]
        rows = rows + all_odds
    
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

df.to_csv(path.join(DATA_DIR, 'scraped_odds_data_2021_compressed.csv'))