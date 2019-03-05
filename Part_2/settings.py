
player_set = {
    # average "true rating"
    'initial':100,
    # standard deviation of player ratings
    'std_dev': 4
}

league_set = {
    'size':64,
    'per_week':32
}

game_set = {
    # game by game score variation amount
    # higher means more upsets
    'var':10
}


elo_set = {
    'initial': 1500,
    'K': 9,
    'beta':400
}

glicko_set = {
    'initial': 1500,
    'RD': 350,
    'tau': 0.5,
    'vol': .06
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
    'RD': 300,
    'tau': 0.5,
    'vol': .06,
    'preseason': 2
}




# end
