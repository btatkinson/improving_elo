import numpy as np
import pandas as pd
import math

from settings import *

class Elo(object):
    """docstring for Elo."""

    beta = elo_set['beta']
    K = elo_set['K']

    ielo_acp = ielo_set['ACP']
    ielo_c = ielo_set['C']

    def __init__(self, arg=None):
        super(Elo, self).__init__()
        self.arg = arg

    # for reg Elo

    def x(self, t1_elo, t2_elo):
        elo_diff = t1_elo - t2_elo
        return 1/(1 + math.pow(10,(-elo_diff / self.beta)))

    def get_delta(self, prob):
        return self.K * (1 - prob)

    # for improved Elo

    def get_movm(self, margin):
        # return np.log(max(abs(margin), 1) + 1.0)
        return .144*margin

    def get_acp(self, elo_diff):
        return (self.ielo_c / ((elo_diff) * self.ielo_acp + self.ielo_c))

    def get_gamma(self, margin, elo_diff):
        movm = self.get_movm(margin)
        acp = self.get_acp(elo_diff)
        return movm * acp

    def get_k(self,gp):
        k_dict = {
            0:86,
            1:66,
            2:54,
            3:44,
            4:39,
            5:36,
            6:33,
            7:30,
            8:29,
            9:28,
            10:27,
            11:26,
            12:25,
            13:23,
            14:20
        }
        if gp in k_dict.keys():
            x = k_dict[gp]
        else:
            x = 19.5
        return x

    def get_ielo_delta(self, prob, margin, team1, team2):
        gamma = self.get_gamma(margin, (team1.elo-team2.elo))

        t1_K = self.get_k(team1.gp)
        t2_K = self.get_k(team2.gp)

        t1_delta = (t1_K * gamma) * (1 - prob)
        t2_delta = -((t2_K * gamma) * (1 - prob))
        return t1_delta,t2_delta

#end
