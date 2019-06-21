import math

elo_set = {
    'init':1500,
    'beta':400,
    'K':72.5
}

ielo_set = {
    'init':1500,
    # right now, ielo beta doesn't change anything
    'beta':400,
    'ACP':0.0025,
    'C':3.3,
    # how much ratings carry over season to season
    'ratings_overlap':0.69
}

glicko_set = {
    'init':1500,
    'phi':168,
    'sigma':0.06,
    'tau':.03,
    'epsilon':0.000001,
    'resolve_time':3
}

trueskill_set = {
    'mu':25,
    'sigma':4.75,
    'beta':3,
    'tau':0.13,
    'draw_probability':0
}



# end
