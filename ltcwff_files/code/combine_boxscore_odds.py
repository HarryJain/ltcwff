from os import path
import pandas as pd


DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'

teams = {'Atlanta': 'ATL', 'Boston': 'BOS', 'Brooklyn': 'BRK', 'Charlotte': 'CHO', 'Chicago': 'CHI', 'Cleveland': 'CLE', 'Dallas': 'DAL', 'Denver': 'DEN', 'Detroit': 'DET', 'Golden State': 'GSW', 'Houston': 'HOU', 'Indiana': 'IND', 'LA': 'LAC', 'L.A. Lakers': 'LAL', 'LA Lakers': 'LAL', 'LA Clippers': 'LAC', 'L.A. Clippers': 'LAC', 'Memphis': 'MEM', 'Miami': 'MIA', 'Milwaukee': 'MIL', 'Minnesota': 'MIN', 'New Orleans': 'NOP', 'New York': 'NYK', 'Oklahoma City': 'OKC', 'Orlando': 'ORL', 'Philadelphia': 'PHI', 'Phoenix': 'PHO', 'Portland': 'POR', 'Sacramento': 'SAC', 'San Antonio': 'SAS', 'Toronto': 'TOR', 'Utah': 'UTA', 'Washington': 'WAS'}


odds = pd.read_csv(path.join(DATA_DIR, 'scraped_odds_data_2021.csv'))
odds = odds.drop(odds.columns[0], axis = 1)
odds['Team'] = [ teams[team] for team in odds['Team'] ]
odds['Index'] = [ f"{odds.loc[ind, 'Team']}_{odds.loc[ind, 'Date']}" for ind in odds.index ]
odds = odds.set_index('Index')
odds


boxscores = pd.read_csv(path.join(DATA_DIR, 'scraped_nba_boxscores_2021.csv'))
boxscores = boxscores.drop(boxscores.columns[0], axis = 1)
boxscores['Team'] = [ teams[team] for team in boxscores['Team'] ]
boxscores['Index'] = [ f"{boxscores.loc[ind, 'Team']}_{boxscores.loc[ind, 'Date']}" for ind in boxscores.index ]
boxscores = boxscores.set_index('Index')
boxscores


combined = pd.concat([boxscores, odds], axis = 1, join = 'inner')
combined = combined.loc[:, ~combined.columns.duplicated()]
#combined = combined.drop('Date.1', axis = 1)
#combined = combined.drop('Team.1', axis = 1)
print(combined)


combined.to_csv(path.join(DATA_DIR, 'scraped_nba_combined_2021.csv'))