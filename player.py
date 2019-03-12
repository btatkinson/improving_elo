import random
import numpy as np
import pandas as pd

from glicko2 import Glicko2

from settings import *
from faker import Faker

fake = Faker()

class Player(object):

    """This is the Player class."""
    def __init__(self):
        super(Player, self).__init__()
        self.name = fake.name()
        self.initialize_ratings()
        self.initialize_record()
        self.initialize_errors()
        self.mu = self.get_mu()
        self.phi = self.get_phi()
        self.win_pct = self.get_win_pct()
        self.glicko_opps = []
        self.combo_opps = []

    def initialize_ratings(self):

        # variation in player ratings
        std_dev = player_set['std_dev']
        # player rating
        self.rating = random.gauss(player_set['initial'], std_dev)

        # inaccuracy of preseason ratings
        pre_sd = prior_set['preseason']
        # preseason rating
        self.prior = random.gauss(self.rating, pre_sd)
        # convert prior to elo rating
        # found with linear regression
        self.prior = (self.prior*43.051 - 2792.5)

        # elo
        self.elo = elo_set['initial']

        # elo + margin of victory
        self.mov = elo_set['initial']

        # glicko
        self.glicko = glicko_set['initial']
        self.RD = glicko_set['RD']
        self.vol = glicko_set['vol']

        # combo
        pre_sd = combo_set['preseason']
        self.combo = random.gauss(self.rating, pre_sd)
        self.combo = (self.combo*43.051 - 2792.5)
        self.cRD = combo_set['RD']
        self.cVol = combo_set['vol']

        return

    def initialize_record(self):
        self.wins = 0
        self.losses = 0
        self.ties = 0
        # games_played
        self.gp = 0
        return

    def initialize_errors(self):
        self.wl_error = 0
        self.wlm_error = 0
        self.elo_error = 0
        self.prior_error = 0
        self.mov_error = 0
        self.glicko_error = 0
        self.combo_error = 0
        return

    def get_mu(self):
        return (self.glicko-1500)/173.7178

    def get_phi(self):
        return self.RD/173.7178

    def get_win_pct(self):
        if self.gp > 0:
            return (self.wins + 0.5*self.ties)/self.gp
        else:
            return 0.5

    ##############
    ## Trackers ##
    ##############
    def add_gp(self):
        self.gp += 1
        return

    def add_win(self):
        self.wins += 1
        self.win_pct = self.get_win_pct()
        return

    def add_loss(self):
        self.losses += 1
        self.win_pct = self.get_win_pct()
        return

    def add_tie(self):
        self.ties += 1
        self.win_pct = self.get_win_pct()
        return

    def add_errors(self, result, error_dict):
        self.wl_error += ((result - error_dict["wl"])**2)
        self.wlm_error += ((result - error_dict["wlm"])**2)
        self.elo_error += ((result - error_dict["elo"])**2)
        self.prior_error += ((result - error_dict["prior"])**2)
        self.mov_error += ((result - error_dict["mov"])**2)
        self.glicko_error += ((result - error_dict["glicko"])**2)
        self.combo_error += ((result - error_dict["combo"])**2)


        return

    def add_glicko_opp(self, opp):
        self.glicko_opps.append(opp)
        return

    def add_combo_opp(self, opp):
        self.combo_opps.append(opp)
        return

    def resolve_glicko(self):
        env = Glicko2(tau=glicko_set['tau'])
        player_rating = env.create_rating(self.glicko, self.RD, self.vol)
        new_rating = env.rate(player_rating, self.glicko_opps)
        self.glicko = new_rating.glicko
        self.RD = new_rating.RD
        self.vol = new_rating.vol
        self.glicko_opps = []
        return new_rating

    def resolve_combo(self):
        env = Glicko2(tau=combo_set['tau'])
        player_rating = env.create_rating(self.combo, self.cRD, self.cVol)
        new_rating = env.rate(player_rating, self.combo_opps)
        self.combo = new_rating.glicko
        self.cRD = new_rating.RD
        self.cVol = new_rating.vol
        self.combo_opps = []
        return


# end
