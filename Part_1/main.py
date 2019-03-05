import numpy as np
import pandas as pd
import random

from elo import Elo
from player import Player
from schedule import Schedule
from settings import *

from faker import Faker
from tqdm import tqdm
from sklearn.metrics import brier_score_loss

fake = Faker()

def play_games(schedule):

    k = elo_settings['K']
    beta = elo_settings['beta']
    home_advantage = elo_settings['home_advantage']
    mov = elo_settings['mov']

    elo = Elo(k, beta, home_advantage)

    game_var = season_settings['game_var']
    skill_gap = schedule_settings['skill_gap_cutoff']

    # if skip is true, skill gap too large will not record data
    skip = False

    for gp, i in tqdm(enumerate(range(schedule.num_games))):
        matchups = schedule.create_matchups()

        players = []
        for matchup in matchups:
            p1 = matchup[0]
            p2 = matchup[1]

            # get necessary variables
            p1_elo = p1.elo
            p2_elo = p2.elo
            p1_rtg = p1.rtg
            p2_rtg = p2.rtg
            p1_game_score = int(np.round(random.gauss(p1.rtg,game_var),0))
            p2_game_score = int(np.round(random.gauss(p2.rtg,game_var),0))

            # log a game as played
            p1.played_game()
            p2.played_game()

            # figure out outcome
            if p1_game_score > p2_game_score:
                p1.add_error(p2.elo, p2.mov_elo, 1)
                p2.add_error(p1.elo, p1.mov_elo, 0)
                p1.add_win()
                p2.add_loss()
            elif p2_game_score > p1_game_score:
                p1.add_error(p2.elo, p2.mov_elo, 0)
                p2.add_error(p1.elo, p1.mov_elo, 1)
                p1.add_loss()
                p2.add_win()
            else:
                p1.add_error(p2.elo, p2.mov_elo, 0.5)
                p2.add_error(p1.elo, p1.mov_elo, 0.5)
                p1.add_tie()
                p2.add_tie()

            # elo calculations
            new_elo1, new_elo2 = elo.rate(p1_elo, p2_elo, p1_rtg, p2_rtg)
            if mov:
                new_mov1, new_mov2 = elo.rate_mov(p1_elo, p2_elo, p1_rtg, p2_rtg)
                p1.mov_elo = new_mov1
                p2.mov_elo = new_mov2

            p1.elo = new_elo1
            p2.elo = new_elo2

            p1.nudge_rating()
            p2.nudge_rating()

            players.append(p1)
            players.append(p2)

        # after series of games is played, refresh league with updated players
        schedule.players = players

        # check on skill_gap
        p_max = 0
        p_min = season_settings['avg_rtg']
        for p in players:
            rtg = p.rtg
            if p_max < rtg:
                p_max = rtg
            elif p_min > rtg:
                p_min = rtg

        if p_max - p_min > skill_gap:
            print("Season was cut short after " + str(gp) + " games because of skill gap")
            skip = True
            break

    # assemble league table
    table_array = []
    for p in schedule.players:
        table_array.append([p.name, p.rtg, p.wins, p.losses, p.ties, p.elo, p.mov_elo,
        p.wl_error, p.elo_error, p.mov_error])

    columns = ['Name', 'True Rating', 'Wins', 'Losses', 'Ties', 'Elo', 'Mov_Elo', 'WL Error', 'Elo Error', 'MOV Error']
    league_table = pd.DataFrame(table_array, columns=columns)
    league_table = league_table.sort_values(by='True Rating',ascending=False)

    return skip, league_table, gp

def create_league(size, avg_rtg, std_dev):

    table_array = []
    league = []
    for p in range(size):
        # initialize player
        player_name = fake.name()

        # assign random initial true ratings
        player_rtg = random.gauss(avg_rtg, std_dev)
        player_elo = mov_elo = elo_settings['init_elo']

        player_entry = [player_name, player_rtg, 0, 0, 0, player_elo, mov_elo]
        table_array.append(player_entry)

        new_player = Player(player_name, player_rtg, player_elo, mov_elo)
        league.append(new_player)

    league_table = pd.DataFrame(table_array, columns=['Name', 'True Rating', 'Wins', 'Losses', 'Ties', 'Elo', 'MOV_Elo'])
    league_table = league_table.sort_values(by='True Rating', ascending=False)
    return league, league_table

def run_season():

    ###################
    ## create league ##
    ###################

    league_size = season_settings['num_players']
    # average player rating
    avg_rating = season_settings['avg_rtg']
    # distribution of player skill
    skill_var = season_settings['std_dev']

    players, league_table = create_league(league_size, avg_rating, skill_var)

    print(league_table)

    ###################
    ## load schedule ##
    ###################

    num_games = schedule_settings['num_games']

    # choose whether to have a skill gap cutoff
    skill_gap_cutoff = schedule_settings['skill_gap_cutoff']

    # choose whether to have day by day skill nudges
    # alternative is game by game
    day_by_day = schedule_settings['day_by_day']
    schedule = Schedule(players, num_games, skill_gap_cutoff, day_by_day)

    ################
    ## Play Games ##
    ################

    skip, final_table, games_played = play_games(schedule)

    if skip:
        return 0,0

    total_wl_error = final_table['WL Error'].sum()
    total_elo_error = final_table['Elo Error'].sum()
    total_mov_error = final_table['MOV Error'].sum()

    avg_wl_error = np.round(total_wl_error/games_played/season_settings['num_players']/2,4)
    avg_elo_error = np.round(total_elo_error/games_played/season_settings['num_players']/2,4)
    avg_mov_error = np.round(total_mov_error/games_played/season_settings['num_players']/2,4)

    print("Win-Loss Error: " + str(avg_wl_error))
    print("Elo Error: " + str(avg_elo_error))
    print("Elo + Margin of Victory: " + str(avg_mov_error))

    final_table = final_table.round(2)

    print(final_table)

    return avg_elo_error, avg_mov_error


if __name__ == "__main__":

    run_season()

    # multiple seasons used for testing parameters
    # print("Starting...")
    # table_array = []
    # for i in range(146):
    #     num_games = 16 + i
    #     for j in range(5):
    #         elo_error, mov_error = run_season(num_games)
    #         table_array.append([num_games, elo_error, mov_error])
    #
    # df = pd.DataFrame(table_array, columns=['Num Games', 'Elo Error', 'ELO + MOV'])
    # df.to_csv('./data.csv', index=False)
















# end
