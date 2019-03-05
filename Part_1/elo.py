import numpy as np
import pandas as pd

from settings import *

class Elo(object):
    """docstring for Elo."""
    def __init__(self, k, beta, home_advantage):
        super(Elo, self).__init__()
        self.k = k
        self.beta = beta
        self.home_advantage = home_advantage

    def expected_prob(self, elo_diff):
        return 1 / (1 + 10 ** (-elo_diff / self.beta))

    def result(self, p1_score, p2_score):
        if p1_score > p2_score:
            result = 1
        elif p1_score < p2_score:
            result = 0
        else:
            result = 0.5
        return result

    def rate(self, p1, p2, p1_score, p2_score):
        # p1 is home
        elo_diff = p1 - p2 + (self.home_advantage)
        # predicted probability
        prob = self.expected_prob(elo_diff)
        # actual result
        result = self.result(p1_score, p2_score)
        # amount of Elo change
        delta = self.k * (result - prob)
        new_p1 = p1 + delta
        new_p2 = p2 - delta
        return new_p1, new_p2

    def rate_mov(self, p1, p2, p1_score, p2_score):
        ### these steps are same as regular rate ###
        elo_diff = p1 - p2 + (self.home_advantage)
        prob = self.expected_prob(elo_diff)
        result = self.result(p1_score, p2_score)

        ### add a margin of victory multiplier ###
        margin = abs(p1-p2)
        # use a natural log func to increase k
        multiplier = np.log(max(margin, 1) + 1.0)
        # need a term to prevent autocorrelation!
        # taken from 538's implementation
        # better teams receive less multiplier
        # put another way, the higher elo diff gets, the smaller ac_prevent gets
        ac_prevent = (2.2 / (1.0 if result == 0.5 else ((elo_diff if result == 1.0 else -elo_diff) * 0.001 + 2.2)))
        gamma = multiplier * ac_prevent
        # gamma = multiplier
        delta = (self.k * gamma) * (result - prob)
        new_p1 = p1 + delta
        new_p2 = p2 - delta
        return new_p1, new_p2




# end
