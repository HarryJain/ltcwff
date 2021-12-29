# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 19:35:30 2021

@author: Harry
"""

# Module Imports
import pandas as pd
from os import path
from bs4 import BeautifulSoup as Soup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from datetime import date


# Global Variables
DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data\\daily_predictions'

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

team_names = {'Atlanta': 'ATL', 'Boston': 'BOS', 'Brooklyn': 'BRK', 'Charlotte': 'CHO', 'Chicago': 'CHI', 'Cleveland': 'CLE', 'Dallas': 'DAL', 'Denver': 'DEN', 'Detroit': 'DET', 'Golden State': 'GSW', 'Houston': 'HOU', 'Indiana': 'IND', 'LA': 'LAC', 'L.A. Lakers': 'LAL', 'LA Lakers': 'LAL', 'LA Clippers': 'LAC', 'L.A. Clippers': 'LAC', 'Memphis': 'MEM', 'Miami': 'MIA', 'Milwaukee': 'MIL', 'Minnesota': 'MIN', 'New Orleans': 'NOP', 'New York': 'NYK', 'Oklahoma City': 'OKC', 'Orlando': 'ORL', 'Philadelphia': 'PHI', 'Phoenix': 'PHO', 'Portland': 'POR', 'Sacramento': 'SAC', 'San Antonio': 'SAS', 'Toronto': 'TOR', 'Utah': 'UTA', 'Washington': 'WAS'}


# Get Daily Odds Data
def get_daily_odds(current_date, period = '', period_formatted = ''):
    print(period)
    
    all_rows = []
    
    spread_url = f'https://classic.sportsbookreview.com/betting-odds/nba-basketball/{period}/?date={current_date}'

    driver.get(spread_url)
    
    spread_soup = Soup(driver.page_source, 'html.parser')
    
    all_game_spreads = spread_soup.find('div', {'class': 'eventLines'})
    #print(all_game_spreads)
    
    if all_game_spreads == None:
        return

    all_game_spreads = all_game_spreads.find_all('div', {'class': 'event-holder holder-scheduled'})
    
    for game in all_game_spreads:
        row_1 = {}
    
        teams = [ x.string for x in game.find('div', {'class': 'el-div eventLine-team'}).find_all('a') ]
        book = 0
        spreads = None
        while spreads == None:
            try:
                spreads = [ x.string for x in game.find_all('div', {'class': 'el-div eventLine-book'})[book].find_all('div') ]
            except:
                break
            book += 1
        
        row_1['Date'] = current_date
        row_1['Home Team'] = team_names[teams[0]]
        row_1['Away Team'] = team_names[teams[1]]
        
        if spreads[0] != None:
            spread_1 = spreads[0].split('\xa0')
            if len(spread_1) == 1 and spreads[0][0:2] == 'PK':
                spread_1 = ['0', spreads[0][2:]]
                
            row_1[f'Home {period_formatted}Spread'] = float(spread_1[0]) if len(spread_1[0].split('½')) == 1 else float(f"{spread_1[0].split('½')[0]}.5")
            row_1[f'Home {period_formatted}Spread Odds'] = int(spread_1[1])
        else:
            row_1[f'Home {period_formatted}Spread'] = None
            row_1[f'Home {period_formatted}Spread Odds'] = None
            
        if spreads[1] != None:
            spread_2 = spreads[1].split('\xa0')
            if len(spread_2) == 1 and spreads[1][0:2] == 'PK':
                spread_2 = ['0', spreads[1][2:]]
                
            row_1[f'Away {period_formatted}Spread'] = float(spread_2[0]) if len(spread_2[0].split('½')) == 1 else float(f"{spread_2[0].split('½')[0]}.5")
            row_1[f'Away {period_formatted}Spread Odds'] = int(spread_2[1])
        else:
            row_1[f'Away {period_formatted}Spread'] = None
            row_1[f'Away {period_formatted}Spread Odds'] = None
        
        all_rows.append(row_1)
        
    ml_url = f'https://classic.sportsbookreview.com/betting-odds/nba-basketball/money-line/{period}/?date={current_date}'

    driver.get(ml_url)
    
    ml_soup = Soup(driver.page_source, 'html.parser')
    
    all_game_mls = ml_soup.find('div', {'class': 'eventLines'})
    if all_game_mls == None:
        return
    
    all_game_mls = all_game_mls.find_all('div', {'class': 'event-holder holder-scheduled'})
    
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
        
        all_rows[i][f'Home {period_formatted}ML'] = int(mls[0]) if mls[0] != None else None
        all_rows[i][f'Away {period_formatted}ML'] = int(mls[1]) if mls[1] != None else None
        
        i += 1
        
        
    total_url = f'https://classic.sportsbookreview.com/betting-odds/nba-basketball/totals/{period}/?date={current_date}'

    driver.get(total_url)
    
    total_soup = Soup(driver.page_source, 'html.parser')
    
    all_game_totals = total_soup.find('div', {'class': 'eventLines'})
    if all_game_totals == None:
        return
    
    all_game_totals = all_game_totals.find_all('div', {'class': 'event-holder holder-scheduled'})
    
    i = 0
    for game in all_game_totals:
        book = 0
        totals = None
        while totals == None:
            try:
                totals = [ x.string for x in game.find_all('div', {'class': 'el-div eventLine-book'})[book].find_all('b') ]
            except:
                book += 1
        
        if totals[0] != None:
            over = totals[0].split('\xa0')
            all_rows[i][f'{period_formatted}Over'] = float(over[0]) if len(over[0].split('½')) == 1 else float(f"{over[0].split('½')[0]}.5")
            all_rows[i][f'{period_formatted}Over Odds'] = int(over[1])
        else:
            all_rows[i][f'{period_formatted}Over'] = None
            all_rows[i][f'{period_formatted}Over Odds'] = None
            
        if totals[1] != None:
            under = totals[1].split('\xa0')
            all_rows[i][f'{period_formatted}Under'] = float(under[0]) if len(under[0].split('½')) == 1 else float(f"{under[0].split('½')[0]}.5")
            all_rows[i][f'{period_formatted}Under Odds'] = int(under[1])
        else:
            all_rows[i][f'{period_formatted}Under'] = None
            all_rows[i][f'{period_formatted}Under Odds'] = None
        
        i += 1
                
    return all_rows


# Get Odds for Today
rows = []

today = date.today()
datef = today.strftime("%Y%m%d")
print(datef)

odds = get_daily_odds(datef)
odds

if odds != None:
    all_odds = []
    for i in range(len(odds)):
        all_odds.append(odds[i])
    rows = rows + all_odds
    
df = pd.DataFrame(rows)
print(df)
df.iloc[:, [1, 2, 7, 8]]


# Log predictions
i = 0
while i < len(df.index):
    # Header
    print(f"{df.iloc[i, 1]} vs. {df.iloc[i, 2]}")
    print("")
    
    
    # Spread Prediction
    print(f"Spread: {df.iloc[i, 1]} {df.iloc[i, 3]}", end = "")
    
    spread_prediction = input(f"Prediction ({df.iloc[i, 1]} or {df.iloc[i, 2]}): ")
    while spread_prediction != df.iloc[i, 1] and spread_prediction != df.iloc[i, 2]:
        spread_prediction = input(f"Prediction ({df.iloc[i, 1]} or {df.iloc[i, 2]}): ")
    df.loc[df.index[i], 'Spread Prediction'] = spread_prediction
    
    spread_confidence = input("Confidence (1-5): ")
    while int(spread_confidence) > 5 or int(spread_confidence) < 1:
        spread_confidence = input("Confidence (1-5): ")
    df.loc[df.index[i], 'Spread Confidence'] = spread_confidence
    
    print("\n")
    
    
    # Total Prediction
    print(f"Total: {df.iloc[i, 9]}", end = "")
    
    total_prediction = input("Prediction (Over or Under): ")
    while total_prediction != "Over" and total_prediction != "Under":
        total_prediction = input("Prediction (Over or Under): ")
    df.loc[df.index[i], 'Total Prediction'] = total_prediction
    
    total_confidence = input("Confidence (1-5): ")
    while int(total_confidence) > 5 or int(total_confidence) < 1:
        total_confidence = input("Confidence (1-5): ")
    df.loc[df.index[i], 'Total Confidence'] = total_confidence
    
    print("\n")
    
    
    # Moneyline Prediction
    print(f"Moneyline: {df.iloc[i, 1]} {df.iloc[i, 7]}, {df.iloc[i, 2]} {df.iloc[i, 8]}", end = "")
    
    ml_prediction = input(f"Prediction ({df.iloc[i, 1]} or {df.iloc[i, 2]}): ")
    while ml_prediction != df.iloc[i, 1] and ml_prediction != df.iloc[i, 2]:
        ml_prediction = input(f"Prediction ({df.iloc[i, 1]} or {df.iloc[i, 2]}): ")
    df.loc[df.index[i], 'ML Prediction'] = ml_prediction
    
    ml_confidence = input("Confidence (1-5): ")
    while int(ml_confidence) > 5 or int(ml_confidence) < 1:
        ml_confidence = input("Confidence (1-5): ")
    df.loc[df.index[i], 'ML Confidence'] = ml_confidence
    
    print("\n\n")
    
    
    i += 1
    

df['Index'] = [ f"{df.loc[ind, 'Date']}_{df.loc[ind, 'Home Team']}_{df.loc[ind, 'Away Team']}" for ind in df.index ]
df = df.set_index('Index')
print(df)


all_predictions = pd.read_csv(path.join(DATA_DIR, 'daily_predictions.csv'))
all_predictions = all_predictions.set_index('Index')
all_predictions = pd.concat([all_predictions, df])
all_predictions = all_predictions[~all_predictions.index.duplicated(keep = 'last')]
all_predictions.to_csv(path.join(DATA_DIR, "daily_predictions.csv"))
