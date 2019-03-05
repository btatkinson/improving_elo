import numpy as np
import pandas as pd

from settings import *
import random


class Player(object):

    nudge = schedule_settings['rtg_nudge']
    beta = elo_settings['beta']

    """Player Object"""
    def __init__(self, name, rtg, elo, mov_elo):
        super(Player, self).__init__()
        self.name = name

        # true rating
        self.rtg = rtg

        # elo rating
        self.elo = elo

        # margin of victory elo
        self.mov_elo = elo

        # wins, losses, ties
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.games_played = 0

        # error trackers
        self.mov_error = 0
        self.elo_error = 0
        self.wl_error = 0

    def nudge_rating(self):
        # decide to nudge up or down
        direction = random.randint(0,1)
        if direction == 0:
            self.rtg += self.nudge
        else:
            self.rtg -= self.nudge

    def add_win(self):
        self.wins += 1

    def add_loss(self):
        self.losses += 1

    def add_tie(self):
        self.ties += 1

    def played_game(self):
        self.games_played += 1

    def expected_prob(self, elo_diff):
        return 1 / (1 + 10 ** (-elo_diff / self.beta))

    def add_error(self, opp_rtg, opp_mov_rtg, result):
        # compare result to predicted probabilities
        # add the error to the error trackers
        elo_diff = self.elo - opp_rtg
        mov_diff = self.mov_elo - opp_mov_rtg

        elo_expect = self.expected_prob(elo_diff)
        mov_expect = self.expected_prob(mov_diff)
        wl_expect = (self.wins + 0.5* self.ties)/self.games_played

        elo_e = (elo_expect - result) ** 2
        mov_e = (mov_expect - result) ** 2
        wl_e = (wl_expect - result) ** 2

        self.elo_error += elo_e
        self.mov_error += mov_e
        self.wl_error += wl_e

        return



#end
