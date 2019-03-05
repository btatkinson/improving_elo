import numpy as np
import pandas as pd
import math

from settings import *

class Elo(object):

    k = elo_set['K']
    beta = elo_set['beta']

    """docstring for Elo."""
    def __init__(self):
        super(Elo, self).__init__()

    def get_expected_prob(self, elo_diff):
        # glitches if I don't use math.pow instead of 10 **
        # I guess bc 10 is an int?
        ep = 1/(1 + math.pow(10,(-elo_diff / self.beta)))
        return ep

    def get_delta(self, result, prob):
        return self.k * (result - prob)

    def get_mov_delta(self, result, prob, gamma):
        return (self.k * gamma) * (result - prob)

    # get margin of victory multiplier
    def get_movm(self, elo_diff):
        return np.log(max(elo_diff, 1) + 1.0)

    def get_acp(self, result, elo_diff):
        return (2.2 / (1.0 if result == 0.5 else ((elo_diff if result == 1.0 else -elo_diff) * 0.001 + 2.2)))

    def get_gamma(self, result, elo_diff):
        movm = self.get_movm(elo_diff)
        acp = self.get_acp(result, elo_diff)
        return movm * acp








#end
