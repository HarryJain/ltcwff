import pandas as pd
from os import path
import sqlite3

###############################################
# loading csvs and putting them in a sqlite db
###############################################

# only need to run this section once

# handle directories
DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'

# create connection
conn = sqlite3.connect(path.join(DATA_DIR, 'fantasy.sqlite'))
test_conn = sqlite3.connect(path.join(DATA_DIR, 'test.sqlite'))

# load csv data
player_game = pd.read_csv(path.join(DATA_DIR, 'game_data_sample.csv'))
player_game.head()
player_game.columns

player = pd.read_csv(path.join(DATA_DIR, 'game_data_player_sample.csv'))
player.head()

game = pd.read_csv(path.join(DATA_DIR, 'game_2017_sample.csv'))
game.head()

team = pd.read_csv(path.join(DATA_DIR, 'teams.csv'))
team.head()

# and write it to sql
player_game.to_sql('player_game', conn, index=False, if_exists='replace')
player.to_sql('player', conn, index=False, if_exists='replace')

game.to_sql('game', conn, index=False, if_exists='replace')
team.to_sql('team', conn, index=False, if_exists='replace')

#########
# Queries
#########
conn = sqlite3.connect(path.join(DATA_DIR, 'fantasy.sqlite'))

# return entire player table
df = pd.read_sql(
    """
    SELECT *
    FROM player
    """, conn)
df.head()
df.shape

# return specific columns from player table + rename on the fly
df = pd.read_sql(
    """
    SELECT player_id, player_name AS name, pos
    FROM player
    """, conn)
df.head()

###########
# filtering
###########

# basic filter, only rows where team is MIA
df = pd.read_sql(
    """
    SELECT player_id, player_name AS name, pos
    FROM player
    WHERE team = 'MIA'
    """, conn)
df.head()

# AND in filter
df = pd.read_sql(
    """
    SELECT player_id, player_name AS name, pos
    FROM player
    WHERE team = 'MIA' AND pos == 'WR'
    """, conn)
df.head()

# OR in filter
df = pd.read_sql(
    """
    SELECT player_id, player_name AS name, pos, team
    FROM player
    WHERE team = 'MIA' OR team == 'NE'
    """, conn)
df.head()

# IN in filter
df = pd.read_sql(
    """
    SELECT player_id, player_name AS name, pos, team
    FROM player
    WHERE team IN ('MIA', 'NE')
    """, conn)
df.head()

# negation with NOT
df = pd.read_sql(
    """
    SELECT player_id, player_name AS name, pos, team
    FROM player
    WHERE team NOT IN ('MIA', 'NE')
    """, conn)
df

#########
# joining
#########

# no WHERE so fullcrossjoin
df = pd.read_sql(
    """
    SELECT
        player.player_name as name,
        player.pos,
        player.team,
        team.conference,
        team.division
    FROM player, team
    """, conn)
df.head(10)
df.shape

# add in two team columns to make clearer
df = pd.read_sql(
    """
    SELECT
        player.player_name as name,
        player.pos,
        player.team as player_team,
        team.team as team_team,
        team.conference,
        team.division
    FROM player, team
    """, conn)
df.head(10)
df.sample(10)

# n of rows
df.shape

# works when we add WHERE to filter after crossjoin
df = pd.read_sql(
    """
    SELECT
        player.player_name as name,
        player.pos,
        player.team,
        team.conference,
        team.division
    FROM player, team
    WHERE player.team = team.team
    """, conn)
df.head()

# add in team column to make clearer how it works
df = pd.read_sql(
    """
    SELECT
        player.player_name as name,
        player.pos,
        player.team as player_team,
        team.team as team_team,
        team.conference,
        team.division
    FROM player, team
    WHERE player.team = team.team
    """, conn)
df.head()

# adding a third table
df = pd.read_sql(
    """
    SELECT
        player.player_name as name,
        player.pos,
        team.team,
        team.conference,
        team.division,
        player_game.*
    FROM player, team, player_game
    WHERE
        player.team = team.team AND
        player_game.player_id = player.player_id
    """, conn)
df.head()

# adding a third table - shorthand
df = pd.read_sql(
    """
    SELECT
        p.player_name as name,
        p.pos,
        t.team,
        t.conference,
        t.division,
        pg.*
    FROM player AS p, team AS t, player_game AS pg
    WHERE
        p.team = t.team AND
        pg.player_id = p.player_id
    """, conn)
df.head()

# adding an additional filter
df = pd.read_sql(
    """
    SELECT
        p.player_name as name,
        p.pos,
        t.team,
        t.conference,
        t.division,
        pg.*
    FROM player AS p, team AS t, player_game AS pg
    WHERE
        p.team = t.team AND
        pg.player_id = p.player_id AND
        p.pos == 'RB'
    """, conn)
df.head()
df.sample(5)

###########
# LIMIT/TOP
###########

# SELECT *
# FROM player
# LIMIT 5

# SELECT TOP 5 *
# FROM player

# testing LIMIT
df = pd.read_sql(
    """
    SELECT
        p.player_name as name,
        p.pos,
        t.team,
        t.conference,
        t.division,
        pg.*
    FROM player AS p, team AS t, player_game AS pg
    WHERE
        p.team = t.team AND
        pg.player_id = p.player_id AND
        p.pos == 'RB'
    LIMIT 5
    """, conn)
df

# DISTINCT
df = pd.read_sql(
    """
    SELECT DISTINCT season, week, date
    FROM game
    """, conn)
df.head()

# UNION
# SELECT *
# FROM player_data_2018
# UNION
# SELECT *
# FROM player_data_2019

# SUBQUERIES

# LEFT, RIGHT, OUTER JOINS

# SELECT *
# FROM <left_table>
# LEFT JOIN <right_table> ON <left_table>.<common_column> = <right_table>.<common_column>

df = pd.read_sql(
    """
    SELECT a.*, b.rec_yards, b.rush_yards, b.rec_tds, b.rush_tds
    FROM
        (SELECT game.season, week, gameid, home as team, player_id, player_name
        FROM game, player
        WHERE game.home = player.team
        UNION
        SELECT game.season, week, gameid, away as team, player_id, player_name
        FROM game, player
        WHERE game.away = player.team) AS a
    LEFT JOIN player_game AS b ON a.gameid = b.gameid AND a.player_id = b.player_id
    """, conn)
df
df.loc[df['player_name'] == 'M.Sanu']

# INNER JOIN
df = pd.read_sql(
    """
    SELECT a.*, b.rec_yards, b.rush_yards, b.rec_tds, b.rush_tds
    FROM
        (SELECT game.season, week, gameid, home as team, player_id, player_name
        FROM game, player
        WHERE game.home = player.team
        UNION
        SELECT game.season, week, gameid, away as team, player_id, player_name
        FROM game, player
        WHERE game.away = player.team) AS a
    JOIN player_game AS b ON a.gameid = b.gameid AND a.player_id = b.player_id
    """, conn)
df
df.loc[df['player_name'] == 'M.Sanu']

###########
# Exercises
###########

# 4.1
# ANS:
# a)
afc_qbs = pd.read_sql(
    '''
    SELECT
        game.season,
        week,
        player_name,
        player_game.team,
        attempts,
        completions,
        pass_yards as yards,
        pass_tds as tds,
        interceptions
    FROM
        player_game, game, team
    WHERE
        player_game.gameid = game.gameid AND
        player_game.team = team.team AND
        conference = 'AFC' AND
        pos = 'QB'
    ''', conn)
# TEST:
afc_qbs
afc_qbs.sample(10)
# b)
afc_qbs_normalized = pd.read_sql(
    '''
    SELECT
        g.season,
        week,
        p.player_name,
        p.team,
        attempts,
        completions,
        pass_yards as yards,
        pass_tds as tds,
        interceptions
    FROM
        player_game as pg, game as g, player as p, team as t
    WHERE
        pg.gameid = g.gameid AND
        pg.player_id = p.player_id AND
        p.team = t.team AND
        conference = 'AFC' AND
        p.pos = 'QB'
    ''', conn)
# TEST:
afc_qbs
afc_qbs.sample(10)

# 4.2
# ANS:
game_plus = pd.read_sql(
    '''
    SELECT
        game.*,
        home_team.mascot as home_mascot,
        away_team.mascot as away_mascot
    FROM
        game, team as home_team, team as away_team
    WHERE
        game.home = home_team.team AND
        game.away = away_team.team
    ''', conn)
# TEST:
game_plus
game_plus.sample(5)
