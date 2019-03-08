import numpy as np
import pandas as pd

from settings import *
from player import Player
from game import Game
from schedule import Schedule
from glicko2 import Glicko2

from tqdm import tqdm

def create_players(league_size):

    players = []
    for p in range(league_size):
        player = Player()
        players.append(player)

    return players

def play_games(matchups):
    schedule = Schedule()
    players_played = []
    for matchup in matchups:
        p1 = matchup[0]
        p2 = matchup[1]
        game = Game(p1, p2)
        p1, p2 = game.play_game()
        matchup = schedule.nudge_ratings(matchup)
        players_played.append(matchup[0])
        players_played.append(matchup[1])
    return players_played

def calc_error(players, week):
    ppw = schedule_set['players_per_week']
    num_games = (ppw * week)/2

    wl_error = 0
    wlm_error = 0
    elo_error = 0
    prior_error = 0
    mov_error = 0
    glicko_error = 0
    combo_error = 0
    for player in players:
        wl_error += player.wl_error
        wlm_error += player.wlm_error
        elo_error += player.elo_error
        prior_error += player.prior_error
        mov_error += player.mov_error
        glicko_error += player.glicko_error
        combo_error += player.combo_error

    # divide by 2 because averaging error between two players in game
    wl_error = (wl_error/num_games/2)
    wlm_error = (wlm_error/num_games/2)
    elo_error = (elo_error/num_games/2)
    prior_error = (prior_error/num_games/2)
    mov_error = (mov_error/num_games/2)
    glicko_error = (glicko_error/num_games/2)
    combo_error = (combo_error/num_games/2)

    return [week, wl_error, wlm_error, elo_error, prior_error,
    mov_error, glicko_error, combo_error]

def run_season():

    # import season settings
    league_size = league_set['size']

    # create players
    players = create_players(league_size)


    cols = ['Name', 'Rating', 'Prior', 'Elo', 'MOV', 'Glicko',
    'RD', 'Vol', 'Combo', 'cRD','cVol',
    'Wins', 'Losses', 'Ties', 'Games Played', 'WL Error', 'WLM Error',
    'Elo Error', 'Prior Error', 'MOV Error', 'Glicko Error', 'Combo Error',
    'Mu', 'Phi', 'Win Pct','G_OPPS','C_OPPS']
    table_array = []
    for player in players:
        player_dict = player.__dict__
        player_entry = list(player_dict.values())
        table_array.append(player_entry)

    df = pd.DataFrame(table_array, columns=cols)
    df = df.sort_values(by='Rating', ascending=False)

    df = df[['Name', 'Rating', 'Prior', 'Elo', 'MOV', 'Glicko', 'Combo']]
    print(df.head())

    # create schedule
    # must create rating periods for Glicko
    schedule = Schedule()
    calendar = schedule.create_calendar()

    # keep track of error throughout season
    error_array = []

    for day_num, day in tqdm(enumerate(calendar)):
        if day == "OFF":
            players = schedule.nudge_ratings(players)
        elif day == "GAMES":
            matchups,players_off = schedule.create_matchups(players)
            players_off = schedule.nudge_ratings(players_off)
            players_played = play_games(matchups)
            players = players_off + players_played
        else:
            matchups,players_off = schedule.create_matchups(players)
            players_off = schedule.nudge_ratings(players_off)
            players_played = play_games(matchups)
            players = players_off + players_played
            for player in players:
                player.resolve_glicko()
                player.resolve_combo()

        # at the end of the week, add up all the errors
        if (day_num + 1) % 7 == 0:
            week = (day_num+1)/7
            error_entry = calc_error(players, week)
            error_array.append(error_entry)

    error_table = pd.DataFrame(error_array, columns=['Week', 'WL', 'WLM', 'Elo', 'Prior',
    'MOV', 'Glicko', 'Combo'])

    error_table.to_csv('Error_Analysis.csv', index=False)

    table_array = []
    for player in players:
        player_dict = player.__dict__
        player_entry = list(player_dict.values())
        table_array.append(player_entry)

    df = pd.DataFrame(table_array, columns=cols)
    df = df.drop(columns=["G_OPPS","C_OPPS"])
    df = df.sort_values(by='Rating', ascending=False)

    df = df[['Name', 'Rating', 'Prior', 'Elo', 'MOV', 'Glicko', 'Combo']]
    print(df.head())

    return


if __name__ == "__main__":

    run_season()













#end
