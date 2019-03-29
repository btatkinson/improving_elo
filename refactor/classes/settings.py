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
    'ACP':0,
    'C':3.3
}

glicko_set = {
    'init':1500,
    'phi':350,
    'sigma':0.06,
    'tau':1,
    'epsilon':0.000001,
    'resolve_time':4
}

steph_set = {
    'init':1500,
}



# end
