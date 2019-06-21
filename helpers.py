import pandas as pd
import numpy as np

import math
import itertools

import trueskill
from settings import *

# define trueskill environment
ts_env = trueskill.TrueSkill(mu=trueskill_set['mu'],
                    sigma=trueskill_set['sigma'],
                    beta=trueskill_set['beta'],
                    tau=trueskill_set['tau'],
                    draw_probability=trueskill_set['draw_probability'])
ts_env.make_as_global()

def l5_x(pa, pb):
    if pa == pb:
        return 0.5
    return (pa - (pa * pb))/((pa + pb) - (2 * pa * pb))

def calc_error(expected_array, result):
    if result == 1:
        return [-math.log10(p) for p in expected_array]
    else:
        return [-math.log10(1-p) for p in expected_array]

def ts_win_prob(team1, team2):
    delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
    size = len(team1) + len(team2)
    denom = math.sqrt(size * (ts_env.beta * ts_env.beta) + sum_sigma)
    ts = trueskill.global_env()
    return ts.cdf(delta_mu / denom)


# end
