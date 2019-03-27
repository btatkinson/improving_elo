import numpy as np
import pandas as pd

from settings import *

from math import log

def log_loss(true, pred, eps=1e-15):
    p = np.clip(pred, eps, 1-eps)
    if true == 1:
        return -log(p)
    else:
        return -log(1-p)

class Team(object):
    """docstring for Team."""
    def __init__(self, tid):
        super(Team, self).__init__()
        # team id
        self.tid = tid

        self.init_ratings()
        self.init_errors()

    def init_ratings(self):
        self.gp = 0
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.wl = 0.5

        self.elo = elo_set['init']
        self.ielo = ielo_set['init']
        self.glicko = glicko_set['init']
        self.steph = steph_set['init']
        return

    def init_errors(self):
        self.l5err = 0
        self.eloerr = 0
        self.ieloerr = 0
        self.glickoerr = 0
        self.stepherr = 0
        return

    def played_game(self):
        self.gp += 1
        self.calc_win_loss()
        return

    def add_win(self):
        self.wins+=1
        self.played_game()
        return

    def add_loss(self):
        self.losses+=1
        self.played_game()
        return

    def add_tie(self):
        self.ties+=1
        self.played_game()
        return

    def calc_win_loss(self):
        self.wl = (self.wins + 0.5*self.ties)/self.gp
        return

    def update_errors(self, errors):
        self.l5err += errors[0]
        self.eloerr += errors[1]
        self.ieloerr += errors[2]
        self.glickoerr += errors[3]
        self.stepherr += errors[4]
        return
    def update_rating(self, rating, delta):
        if rating == 'elo':
            self.elo += delta
        elif rating == 'ielo':
            self.ielo += delta
        elif rating == 'glicko':
            self.glicko += delta
        elif rating == 'steph':
            self.steph += delta
        return




# end
