
player_set = {
    # average "true rating"
    'initial':100,
    # standard deviation of player ratings
    'std_dev': 4.8
}

league_set = {
    'size':32,
    'max_skill_gap':38
}

schedule_set = {
    'weeks':82,
    'players_per_week':32,
    'daily_nudge':0.1
}

game_set = {
    # game by game score variation amount
    # higher means more upsets
    'var':10
}


elo_set = {
    'initial': 1500,
    'K': 27.5,
    'beta':400
}

mov_set = {
    'initial': 1500,
    'K':9,
    'ACP':0,
    'C':3.3,
    'beta':400
}

glicko_set = {
    'initial': 1500,
    'RD': 100,
    'tau': 4,
    'vol': .06,
    'epsilon':0.000001,
    'ratio':173.7178,
    # suggested is 5-10 games per player, so 10-20 weeks
    'rating_period': 2
}

prior_set = {
    # inaccuracy of preseason ratings (higher -> more inaccurate)
    # usually use about 1/5 of the std_dev
    'preseason': 0.65,
    # should use similar K than Elo, maybe a hair smaller
    'K': 27.45
}

combo_set = {
    'initial': 1500,
    'RD': 100,
    'tau': 4,
    'vol': .06,
    'preseason': 0.65,
    # suggested is 5-10 games per player, so 10-20 weeks
    # 'rating_period': 15
}




# end
