
player_set = {
    # average "true rating"
    'initial':100,
    # standard deviation of player ratings
    'std_dev': 4
}

league_set = {
    'size':64,
}

schedule_set = {
    'weeks':165,
    # suggested is 5-10 games per player, so 10-20 weeks
    'rating_period': 15,
    'players_per_week':32,
    'daily_nudge':0.1
}

game_set = {
    # game by game score variation amount
    # higher means more upsets
    'var':4
}


elo_set = {
    'initial': 1500,
    'K': 7,
    'beta':400
}

mov_set = {
    'K':7
}

glicko_set = {
    'initial': 1500,
    'RD': 350,
    'tau': 0.7,
    'vol': .06,
    'epsilon':0.000001,
    'ratio':173.7178
}

prior_set = {
    # inaccuracy of preseason ratings (higher -> more inaccurate)
    # usually use about half of the std_dev
    'preseason': 2,
    # should use smaller K than Elo
    'K': 7
}

combo_set = {
    'initial': 1500,
    'RD': 350,
    'tau': .7,
    'vol': .06,
    'preseason': 2
}




# end
