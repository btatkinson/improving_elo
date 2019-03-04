import numpy as np
import pandas as pd


season_settings = {
    # must be even number of players
    'num_players':32,
    # average ratings for the teams
    'avg_rtg':100,
    # standard deviation of ratings (higher -> more difference in player skill)
    'std_dev': 4,
    # game by game variation amount:
    'game_var':10
}

schedule_settings = {
    'num_games':82,
    # choose whether every player plays every week
    'players_per_week':32,
    # skill gap that automatically ends the season
    # can be set very high to negate this
    # 24 is a 95% win probability with 10 game var
    'skill_gap_cutoff':24,
    # are player ratings nudged day by day or game by game?
    'day_by_day':False,
    # after each day or game, how much does the true rating change?
    # use a very small value for day to day
    'rtg_nudge':0.28
}


elo_settings = {
    # utilize margin of victory?
    'mov':True,
    'init_elo': 1500,
    'K': 9,
    'beta':400,
    # bonus a home team receives
    # player 1 is always the home team
    # I have not built this in to true rating
    # it will only hurt accuracy unless you do
    'home_advantage':0
}



# end
