##############
# basic python
# v0.0.3
##############

##########################
# how to read this chapter
##########################
1 + 1

##########
# comments
##########

# print the result of 1 + 1
print(1 + 1)

###########
# variables
###########

pts_per_passing_td = 4

pts_per_passing_td
3*pts_per_passing_td

pts_per_passing_td = pts_per_passing_td - 3

pts_per_passing_td

####################
# types of variables
####################

over_under = 48  # int
wind_speed = 22.8  # float

starting_qb = 'Tom Brady'
starting_rb = "Le'Veon Bell"

type(starting_qb)

type(over_under)

team_name = f'{starting_qb}, {starting_rb}, & co.'
team_name

# string methods
'he could go all the way'.upper()

'Chad Johnson'.replace('Johnson', 'Ochocinco')

####################################
# How to figure things out in Python
####################################
'tom brady'.capitalize()

'  tom brady'.lstrip()
'tom brady'

team1_pts = 110
team2_pts = 120

# and these are all bools:
team1_won = team1_pts > team2_pts
team2_won = team1_pts < team2_pts
teams_tied = team1_pts == team2_pts
teams_did_not_tie = team1_pts != team2_pts

type(team1_won)
teams_did_not_tie

# error because test for equality is ==, not =
# teams_tied = (team1_pts = team2_pts)  # commented out since it throws an error

shootout = (team1_pts > 150) and (team2_pts > 150)
at_least_one_good_team = (team1_pts > 150) or (team2_pts > 150)
you_guys_are_bad = not ((team1_pts > 100) or (team2_pts > 100))
meh = not (shootout or at_least_one_good_team or you_guys_are_bad)

###############
# if statements
###############
if team1_won:
  message = "Nice job team 1!"
elif team2_won:
  message = "Way to go team 2!!"
else:
  message = "must have tied!"

message

#################
# container types
#################

# lists
my_roster_list = ['tom brady', 'adrian peterson', 'antonio brown']

my_roster_list[0]
my_roster_list[0:2]
my_roster_list[-2:]

# dicts
my_roster_dict = {'qb': 'tom brady',
                  'rb1': 'adrian peterson',
                  'wr1': 'antonio brown'}

my_roster_dict['qb']
my_roster_dict['k'] = 'mason crosby'

# unpacking
qb, rb = ['tom brady', 'todd gurley']

qb = 'tom brady'
rb = 'todd gurley'

# gives an error - n of variables doesn't match n items in list
# qb, rb = ['tom brady', 'todd gurley', 'julio jones']  # commented out w/ error

#######
# loops
#######

# looping over a list
my_roster_list = ['tom brady', 'adrian peterson', 'antonio brown']

my_roster_list_upper = ['', '', '']
i = 0
for player in my_roster_list:
    my_roster_list_upper[i] = player.title()
    i = i + 1

my_roster_list_upper

for x in my_roster_dict:
    print(f"position: {x}")

for x in my_roster_dict:
   print(f"position: {x}")
   print(f"player: {my_roster_dict[x]}")

for x, y in my_roster_dict.items():
    print(f"position: {x}")
    print(f"player: {y}")

################
# comprehensions
################

# lists
my_roster_list
my_roster_list_proper = [x.title() for x in my_roster_list]
my_roster_list_proper

my_roster_list_proper_alt = [y.title() for y in my_roster_list]

type([x.title() for x in my_roster_list])
[x.title() for x in my_roster_list][:2]

my_roster_last_names = [full_name.split(' ')[1] for full_name in my_roster_list]
my_roster_last_names

my_roster_a_only = [
    x.title() for x in my_roster_list if x.startswith('a')]
my_roster_a_only

# dicts
pts_per_player = {
    'tom brady': 20.7, 'adrian peterson': 10.1, 'antonio brown': 18.5}

pts_x2_per_upper_player = {
    name.upper(): pts*2 for name, pts in pts_per_player.items()}

pts_x2_per_upper_player

sum([1, 2, 3])

sum([pts for _, pts in pts_per_player.items()])

###########
# functions
###########
len(['tom brady', 'adrian peterson', 'antonio brown'])

def over_100_total_yds(rush_yds, rec_yds):
    """
    multi line strings in python are between three double quotes

    it's not required, but the convention is to put what the fn does in one of
    these multi line strings (called "docstring") right away in function

    when you type over_100_total_yds? in the REPL, it shows this docstring

    this function takes rushing, receiving yards, adds them, and returns a bool
    indicating whether they're more than 100 or not
    """
    return rush_yds + rec_yds > 100

# print(rush_yds)  # commented out since it shows an error

def noisy_over_100_total_yds(rush_yds, rec_yds):
    """
    this function takes rushing, recieving yards, adds them, and returns a bool
    indicating whether they're more than 100 or not

    it also prints rush_yds
    """
    print(rush_yds)
    return rush_yds + rec_yds > 100

over_100_total_yds(60, 39)
noisy_over_100_total_yds(84, 32)

def over_100_total_yds_wdefault(rush_yds=0, rec_yds=0):
    """
    this function takes rushing, receiving yards, adds them, and returns a bool
    indicating whether they're more than 100 or not

    if a value for rushing or receiving yards is not entered, it'll default to 0
    """
    return rush_yds + rec_yds > 100

over_100_total_yds_wdefault(92)
over_100_total_yds(92)

def do_to_list(working_list, working_fn, desc):
    """
    this function takes a list, a function that works on a list, and a
    description

    it applies the function to the list, then returns the result along with
    description as a string
    """

    value = working_fn(working_list)

    return f'{desc} {value}'

def last_elem_in_list(working_list):
    """
    returns the last element of a list.
    """
    return working_list[-1]

positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']

do_to_list(positions, last_elem_in_list, "last element in your list:")
do_to_list([1, 2, 4, 8], last_elem_in_list, "last element in your list:")

do_to_list(positions, len, "length of your list:")

do_to_list([2, 3, 7, 1.3, 5], lambda x: 3*x[0], "first element in your list times 3 is:")

# normally imports like this would be at the top of the file
import os

os.cpu_count()

from os import path

# change this to the location of your data
DATA_DIR = '/Users/harry/Documents/LTCWFF/ltcwff-files/data'
path.join(DATA_DIR, 'adp_2017.csv')

###############
# EOC Exercises
###############

# 2.1
# ANS: a, b, d, e

# 2.2
# ANS: 133

# 2.3
# ANS:
def for_the_td(name_1, name_2):
    return f"{name_1} to {name_2} for the td!"
# ANS2:
def for_the_td(player_1, player_2):
    return f'{player_1} to {player_2} for the td!'
# TEST:
for_the_td("Dak", "Zeke")

# 2.4
# ANS: islower probably checks if every character of a string is lowercase
# TEST:
'this is a test'.islower()
'This is a test'.islower()


# 2.5
# ANS:
def is_leveon(name):
    return name.lower() in ["le'veon bell", "leveon bell"]
# ANS2:
def is_leveon(player_name):
    #return player_name.strip().lower().replace("'", '') == 'leveon bell'
    return player_name.lower().replace("'", '') == 'leveon bell'
# TEST:
print(is_leveon("tEst"))
print(is_leveon("lEveon beLL"))
print(is_leveon("l'Eveon beLL"))

# 2.6
# ANS:
def commentary(num):
    return f"{num} is a good score" if num >= 100 else f"{num}'s not that good"
# ANS2:
def commentary(number):
    return f'{number} is a good score' if number >= 100 else f"{number}'s not that good" 
# TEST:
print(commentary(100))
print(commentary(90))

# 2.7
# ANS:
giants_roster = ["Daniel Jones", "Saquon Barkley", "Evan Engram", "OBJ"]
print(giants_roster[0:3])
print(giants_roster[:3])
print(giants_roster[:-1])
print([x for x in giants_roster if x != "OBJ"])
# ANS2:
print([player for player in giants_roster if player != 'OBJ'])
print(giants_roster[0:3])
print(giants_roster[:-1])

# 2.8
# ANS:
league_settings = {"number_of_teams": 12, "ppr": True}
# a)
league_settings["number_of_teams"] = 10
# a2)
league_settings['number_of_teams'] = 10
league_settings
# b)
def toggle_ppr(settings):
    settings["ppr"] = not settings["ppr"]
    return settings
# b2}
def toggle_ppr(league_settings):
    return {setting:(value if setting != 'ppr' else not setting) for setting, value in league_settings.items()}
# TEST:
toggle_ppr(league_settings)
league_settings

# 2.9
# ANS:
league_settings = {"number_of_teams": 12, "ppr": True}
# a) Error because there is no such key
#league_settings["has_a_flex"]
# b) Error because name_of_teams is not a variable (should be in quotes)
#league_settings[number_of_teams]
# c) No error because it will create new key and set its value
league_settings["year founded"] = 2002
# TEST:
league_settings["year founded"]

# 2.10
# ANS:
my_roster_list = ["tom brady", "adrian peterson", "antonio brown"]
# a)
for player in my_roster_list:
    print(player.split(' ')[1])
print([x.split(' ')[1] for x in my_roster_list])
# a2)
for player in my_roster_list:
    print(player.split(' ')[-1].capitalize())
# b)
my_my_roster_dict = { name: len(name) for name in my_roster_list }
# b2)
my_my_roster_dict = { player:len(player) for player in my_roster_list }
# TEST:
my_my_roster_dict

# 2.11
# ANS:
my_roster_dict = { 'qb': 'tom brady', 'rb1': 'adrian peterson', 'wr1': 'davante adams', 'wr2': 'john brown' }
# a)
my_my_roster_list = [ pos for pos, name in my_roster_dict.items() ]
# a2)
my_my_roster_list = [ position for position in my_roster_dict ]
# TEST:
my_my_roster_list
# Solution:
solution_roster_list = [ pos for pos in my_roster_dict ]
solution_roster_list
# b)
ab_roster_list = [ name for pos, name in my_roster_dict.items() if name.split(' ')[-1][0] == 'a' or name.split(' ')[-1][0] == 'b' ]
# b2)
ab_roster_list = [ name for _, name in my_roster_dict.items() if name.split(' ')[-1][0] in ['a', 'b'] ]
# TEST:
ab_roster_list
# Solution:
solution_ab_roster_list = [ name for _, name in my_roster_dict.items() if name.split(' ')[-1][0] in ['a', 'b']]
solution_ab_roster_list

# 2.12
# ANS:
# a)
def mapper(alist, afunction):
    return [ afunction(x) for x in alist ]
# a2)
def mapper(alist, afunction):
    return [ afunction(aelement) for aelement in alist ]
# b)
list_of_rushing_yds = [1, 110, 60, 4, 0, 0, 0]
pts_list = mapper(list_of_rushing_yds, lambda x: x / 10)
# b2)
list_of_rushing_yds = [1, 110, 60, 4, 0, 0, 0]
pts_list = mapper(list_of_rushing_yds, lambda x: x * 0.1)
# TEST:
pts_list
