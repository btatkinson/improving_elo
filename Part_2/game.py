import numpy as np
import pandas as pd
import random

from settings import *
from elo import Elo

from sklearn.metrics import brier_score_loss

class Game(object):
    var = game_set['var']
    """docstring for Game."""
    def __init__(self, player1, player2):
        super(Game, self).__init__()
        self.p1 = player1
        self.p2 = player2

    #####################
    ## Error Functions ##
    #####################

    def wl_error(self):

        p1_pred =  self.p1.get_win_pct()
        p2_pred =  self.p2.get_win_pct()

        p1_mpred = (p1_pred + (1-p2_pred))/2
        p2_mpred = (p2_pred + (1-p1_pred))/2

        self.p1_wle = brier_score_loss([self.p1_outcome],[p1_pred])
        self.p2_wle = brier_score_loss([self.p2_outcome],[p2_pred])

        self.p1_wlme = brier_score_loss([self.p1_outcome],[p1_mpred])
        self.p2_wlme = brier_score_loss([self.p2_outcome],[p2_mpred])

        return

    def elo_error(self):
        elo = Elo()
        p1_elo_diff = self.p1.elo - self.p2.elo
        p2_elo_diff = -1 * p1_elo_diff

        p1_pred = elo.get_expected_prob(p1_elo_diff)
        p2_pred = elo.get_expected_prob(p2_elo_diff)

        # update players
        delta = elo.get_delta(self.p1_outcome, p1_pred)
        self.p1.elo += delta
        self.p2.elo -= delta

        self.p1_eloe = brier_score_loss([self.p1_outcome],[p1_pred])
        self.p2_eloe = brier_score_loss([self.p2_outcome],[p2_pred])

        return

    def prior_error(self):
        # same as elo error, just uses prior ratings
        elo = Elo()
        p1_prior_diff = self.p1.prior - self.p2.prior
        p2_prior_diff = -1 * p1_prior_diff

        p1_pred = elo.get_expected_prob(p1_prior_diff)
        p2_pred = elo.get_expected_prob(p2_prior_diff)

        # update players
        delta = elo.get_delta(self.p1_outcome, p1_pred)
        self.p1.prior += delta
        self.p2.prior -= delta

        self.p1_priore = brier_score_loss([self.p1_outcome],[p1_pred])
        self.p2_priore = brier_score_loss([self.p2_outcome],[p2_pred])
        return

    def mov_error(self):
        elo = Elo()
        p1_mov_diff = self.p1.mov - self.p2.mov
        p2_mov_diff = -1 * p1_mov_diff

        p1_pred = elo.get_expected_prob(p1_mov_diff)
        p2_pred = elo.get_expected_prob(p2_mov_diff)

        # update players
        gamma = elo.get_gamma(self.p1_outcome, p1_mov_diff)
        delta = elo.get_mov_delta(self.p1_outcome, p1_pred, gamma)
        self.p1.mov += delta
        self.p2.mov -= delta

        self.p1_move = brier_score_loss([self.p1_outcome],[p1_pred])
        self.p2_move = brier_score_loss([self.p2_outcome],[p2_pred])
        return

    def glicko_error(self):
        return

    def combo_error(self):
        return

    ######################
    ## Update Functions ##
    ######################

    def update_wl(self):
        self.p1.add_gp()
        self.p2.add_gp()
        if self.winner == "P1":
            self.p1.add_win()
            self.p2.add_loss()
        elif self.winner == "P2":
            self.p1.add_loss()
            self.p2.add_win()
        else:
            self.p1.add_tie()
            self.p2.add_tie()
        return

    def update_errors(self):
        print("wl", self.p1_wle)
        print("wlm", self.p1_wlme)
        print("elo", self.p1_eloe)
        print("prior", self.p1_priore)
        print("mov", self.p1_move)
        return

    def play_game(self):
        p1_rtg = self.p1.rating
        p2_rtg = self.p2.rating

        self.p1_score = int(np.round(random.gauss(p1_rtg, self.var),0))
        self.p2_score = int(np.round(random.gauss(p2_rtg, self.var),0))

        print(p1_rtg, p2_rtg)
        print(self.p1_score, self.p2_score)

        if self.p1_score > self.p2_score:
            self.p1_outcome = 1
            self.p2_outcome = 0
            self.winner = "P1"
        elif self.p2_score > self.p1_score:
            self.p2_outcome = 1
            self.p1_outcome = 0
            self.winner = "P2"
        else:
            self.p1_outcome = 0.5
            self.p2_outcome = 0.5
            self.winner = "Tie"

        self.wl_error()
        self.update_wl()

        # these functions also update player objects
        self.elo_error()

        self.prior_error()

        self.mov_error()

        self.glicko_error()

        self.combo_error()

        self.update_errors()

        return self.p1, self.p2








#end
