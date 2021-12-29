from bs4 import BeautifulSoup as Soup
import requests
from pandas import DataFrame

ffc_response = requests.get('https://fantasyfootballcalculator.com/adp/ppr/12-team/all/2017')

print(ffc_response.text)

adp_soup = Soup(ffc_response.text)
adp_soup

# adp_soup is a nested tag, so call find_all on it

tables = adp_soup.find_all('table')

# find_all always returns a list, even if there's only one element, which is
# the case here
len(tables)

# get the adp table out of it
adp_table = tables[0]
adp_table

# adp_table another nested tag, so call find_all again
rows = adp_table.find_all('tr')

# this is a header row
rows[0]

# data rows
first_data_row = rows[1]
first_data_row

first_data_row.find('a').get('href')

# get columns from first_data_row
first_data_row.find_all('td')

# comprehension to get raw data out -- each x is simple tag
[str(x.string) for x in first_data_row.find_all('td')]

# put it in a function
def parse_row(row):
    """
    Take in a tr tag and get the data out of it in the form of a list of
    strings.
    """
    return [str(x.string) for x in row.find_all('td')]

# call function
list_of_parsed_rows = [parse_row(row) for row in rows[1:]]

# put it in a dataframe
df = DataFrame(list_of_parsed_rows)
df.head()

# clean up formatting
df.columns = ['ovr', 'pick', 'name', 'pos', 'team', 'adp', 'std_dev',
              'high', 'low', 'drafted', 'graph']

float_cols = ['adp', 'std_dev']
int_cols = ['ovr', 'drafted']

df[float_cols] = df[float_cols].astype(float)
df[int_cols] = df[int_cols].astype(int)

df.drop('graph', axis=1, inplace=True)

# done
df.head()

###########
# Exercises
###########

# 5.1.1
# ANS:
def scrape_ffc(scoring, nteams, year):
    base_url = 'https://fantasyfootballcalculator.com'
    scoring_string = 'standard/' if scoring == 'std' else 'half-ppr/' if scoring == 'half' else 'ppr/'
    ffc_response = requests.get(f'{base_url}/adp/{scoring_string}{nteams}-team/all/{year}')
    print(f'{base_url}/adp/{scoring_string}{nteams}-team/all/{year}')
    adp_soup = Soup(ffc_response.text)
    data_table = adp_soup.find('table')
    rows = data_table.find_all('tr')
    parsed_rows = [ parse_row_with_link(row) for row in rows[1:] ]
    df = DataFrame(parsed_rows)
    df.columns = [ ' '.join([str(y.string) for y in x.contents if y.string != None]) for x in rows[0].find_all('th') ][:-1] + ['Link']
    return df
# TEST:
scrape_ffc('std', 10, 2020)

# 5.1.2
# ANS:
def parse_row_with_link(row):
    """
    Take in a tr tag and get the data out of it in the form of a list of
    strings, while adding the player link.
    """
    base_url = 'https://fantasyfootballcalculator.com'
    parsed_row = [str(x.string) for x in row.find_all('td')]
    parsed_row[-1] = base_url + row.find('a').get('href')
    return parsed_row
# TEST:
scrape_ffc('half', 12, 2018)

# 5.1.3
# ANS:
def parse_row_to_dict(row):
    """
    Take in a tr tag and get the data out of it in the form of a dictionary of
    the data and its value.
    """
    return {str(row.find('th').string): str(row.find('td').string)}
    
def ffc_player_info(url):
    """
    Takes in a player url, scrapes it, and returns the player's team, height,
    weight, birthday, and draft info (team and pick) as a dict.
    """
    ffc_player_response = requests.get(url)
    player_soup = Soup(ffc_player_response.text)
    name = player_soup.find('h1').string
    team = player_soup.find('h5').contents[0].strip()
    personal_table = player_soup.find_all('table')[0]
    personal_list = [ parse_row_to_dict(row) for row in personal_table.find_all('tr') ]
    personal_dict = { list(dictionary.items())[0][0]:list(dictionary.items())[0][1] for dictionary in personal_list }
    draft_table = player_soup.find_all('table')[1]
    draft_list = [ parse_row_to_dict(row) for row in draft_table.find_all('tr') ]
    draft_dict = { list(dictionary.items())[0][0]:list(dictionary.items())[0][1] for dictionary in draft_list }
    return {
        'Name': name,
        'Team': team,
        'Height': personal_dict['Height'],
        'Weight': personal_dict['Weight'],
        'Birthdate': personal_dict['Birthdate'],
        'Draft Team': draft_dict['Team'],
        'Draft Pick': draft_dict['Pick'].replace('\n', '').strip(),
    }

# SOL (broken):
'''def sol_ffc_player_info(url):
    ffc_response = requests.get(url)
    player_soup = Soup(ffc_response.text)
    
    # info is in multiple tables, but can get all rows with shortcut
    rows = player_soup.find_all('tr')
    
    list_of_parsed_rows = [_parse_player_row(row) for row in rows]
    print(list_of_parsed_rows)
    
    # this is a list of two item lists [[key1, value1], [key2, value2], ...],
    # so we're unpacking each key, value pair with key, value in...
    dict_of_parsed_rows = {key:value for key, value in list_of_parsed_rows}

    # now modify slightly to return what we want, which (per problem
    # instructions) is team, height, weight, birthday, and draft into
    return_dict = {}
    return_dict['team'] = dict_of_parsed_rows['Team:']
    
    return return_dict

def _parse_player_row(row):
    return [str(x.string) for x in row.find_all('td')]
'''

# TEST:
ffc_player_info(scrape_ffc('half', 12, 2018).loc[0, 'Link'])
