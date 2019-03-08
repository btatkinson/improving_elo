import numpy as np
import pandas as pd
import random

from settings import *
from elo import Elo
from glicko2 import Glicko2

from sklearn.metrics import brier_score_loss

# methods to track
# win loss, win loss margin, elo, prior, margin of victory, glicko, combo
methods = ["WL", "WLM", "Elo", "Prior", "MOV", "Glicko", "Combo"]

elo_K = elo_set['K']
prior_K = prior_set['K']
mov_K = mov_set['K']

class Game(object):
    var = game_set['var']
    """docstring for Game."""
    def __init__(self, p1, p2):
        super(Game, self).__init__()
        self.p1 = p1
        self.p2 = p2

        self.p1_rtg = p1.rating
        self.p2_rtg = p2.rating

        # player 1 stats
        self.p1_wl = p1.get_win_pct()
        self.p1_elo = p1.elo
        self.p1_prior = p1.prior
        self.p1_mov = p1.mov
        self.p1_glicko = p1.glicko
        self.p1_combo = p1.combo

        # player 2 stats
        self.p2_wl = p2.get_win_pct()
        self.p2_elo = p2.elo
        self.p2_prior = p2.prior
        self.p2_mov = p2.mov
        self.p2_glicko = p2.glicko
        self.p2_combo = p2.combo

        self.p1_wlm = (self.p1_wl + (1-self.p2_wl)) / 2
        self.p2_wlm = (self.p2_wl + (1-self.p1_wl)) / 2

    def wl_expect(self):
        return self.p1_wl, self.p2_wl, self.p1_wlm, self.p2_wlm

    def elo_expect(self):
        # K doesn't matter here
        env = Elo()

        elo_diff = self.p1_elo - self.p2_elo
        p1_elox = env.get_expected_prob(elo_diff)
        p2_elox = 1-p1_elox

        prior_diff = self.p1_prior - self.p2_prior
        p1_priorx = env.get_expected_prob(prior_diff)
        p2_priorx = 1-p1_priorx

        mov_diff = self.p1_mov - self.p2_mov
        p1_movx = env.get_expected_prob(mov_diff)
        p2_movx = 1-p1_movx
        return p1_elox, p2_elox, p1_priorx, p2_priorx, p1_movx, p2_movx

    def glicko_expect(self):

        env = Glicko2()

        p1 = env.create_rating(self.p1.glicko, self.p1.RD, self.p1.vol)
        p2 = env.create_rating(self.p2.glicko, self.p2.RD, self.p2.vol)

        p1_glickox = env.expected_score(p1,p2)
        p2_glickox = env.expected_score(p2,p1)

        p1 = env.create_rating(self.p1.combo, self.p1.cRD, self.p1.cVol)
        p2 = env.create_rating(self.p2.combo, self.p2.cRD, self.p2.cVol)

        p1_combox = env.expected_score(p1,p2)
        p2_combox = env.expected_score(p2,p1)

        return p1_glickox, p2_glickox, p1_combox, p2_combox

    def play_game(self):

        self.p1_score = int(np.round(random.gauss(self.p1_rtg, self.var),0))
        self.p2_score = int(np.round(random.gauss(self.p2_rtg, self.var),0))

        # get expected results for each system
        p1_wlx, p2_wlx, p1_wlmx, p2_wlmx = self.wl_expect()
        p1_elox, p2_elox, p1_priorx, p2_priorx, p1_movx, p2_movx = self.elo_expect()
        p1_glickox, p2_glickox, p1_combox, p2_combox = self.glicko_expect()

        # get result
        self.p1.add_gp()
        self.p2.add_gp()
        if self.p1_score > self.p2_score:
            self.p1_outcome = 1
            self.p2_outcome = 0
            self.p1.add_win()
            self.p2.add_loss()
        elif self.p2_score > self.p1_score:
            self.p2_outcome = 1
            self.p1_outcome = 0
            self.p2.add_win()
            self.p1.add_loss()
        else:
            self.p1_outcome = 0.5
            self.p2_outcome = 0.5
            self.p1.add_tie()
            self.p2.add_tie()

        # get error of each system and update
        p1_x = {
        "wl":p1_wlx,
        "wlm":p1_wlmx,
        "elo":p1_elox,
        "prior":p1_priorx,
        "mov":p1_movx,
        "glicko":p1_glickox,
        "combo":p1_combox
        }
        p2_x = {
        "wl":p2_wlx,
        "wlm":p2_wlmx,
        "elo":p2_elox,
        "prior":p2_priorx,
        "mov":p2_movx,
        "glicko":p2_glickox,
        "combo":p2_combox
        }

        self.p1.add_errors(self.p1_outcome, p1_x)
        self.p2.add_errors(self.p2_outcome, p2_x)

        elo = Elo()

        # update Elo rankings
        elo_delta = elo.get_delta(self.p1_outcome, p1_elox, elo_K)
        prior_delta = elo.get_delta(self.p1_outcome, p1_priorx, prior_K)
        mov_delta = elo.get_mov_delta(self.p1_outcome, p1_movx, (self.p1.mov-self.p2.mov), mov_K)

        self.p1.elo += elo_delta
        self.p1.prior += prior_delta
        self.p1.mov += mov_delta

        self.p2.elo -= elo_delta
        self.p2.prior -= prior_delta
        self.p2.mov -= mov_delta

        # add Glicko opponents
        env = Glicko2()
        p1_g_opp = env.create_rating(self.p2_glicko,self.p2.RD,self.p2.vol)
        p2_g_opp = env.create_rating(self.p1_glicko,self.p1.RD,self.p1.vol)

        p1_c_opp = env.create_rating(self.p2_combo,self.p2.cRD,self.p2.cVol)
        p2_c_opp = env.create_rating(self.p1_combo,self.p1.cRD,self.p1.cVol)

        self.p1.add_glicko_opp((self.p1_outcome, p1_g_opp))
        self.p2.add_glicko_opp((self.p2_outcome, p2_g_opp))

        self.p1.add_combo_opp((self.p1_outcome, p1_c_opp))
        self.p2.add_combo_opp((self.p2_outcome, p2_c_opp))

        return self.p1, self.p2





# end
