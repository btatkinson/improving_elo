import numpy as np
import pandas as pd
import math

from settings import *

class Elo(object):

    beta = elo_set['beta']
    acp = mov_set['ACP']
    mov_c = mov_set['C']

    """docstring for Elo."""
    def __init__(self,K=7):
        super(Elo, self).__init__()
        self.K = K

    def get_expected_prob(self, elo_diff):
        # glitches if I don't use math.pow instead of 10 **
        # I guess bc 10 is an int?
        ep = 1/(1 + math.pow(10,(-elo_diff / self.beta)))
        return ep

    def get_delta(self, result, prob, K):
        return K * (result - prob)

    def get_mov_delta(self, result, prob, score_diff, elo_diff, K):
        gamma = self.get_gamma(result, score_diff, elo_diff)
        return (K * gamma) * (result - prob)

    # get margin of victory multiplier
    def get_movm(self, score_diff):
        return np.log(max(abs(score_diff), 1) + 1.0)

    def get_acp(self, result, elo_diff):
        return (self.mov_c / (1.0 if result == 0.5 else ((elo_diff if result == 1.0 else -elo_diff) * self.acp + self.mov_c)))

    def get_gamma(self, result, score_diff, elo_diff):
        movm = self.get_movm(score_diff)
        acp = self.get_acp(result, elo_diff)
        return movm * acp








#end
