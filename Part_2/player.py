import random

from settings import *
from faker import Faker

fake = Faker()

class Player(object):

    # import initial settings

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
        self.prior = 

        # elo
        self.elo = elo_set['initial']

        # elo + margin of victory
        self.mov = elo_set['initial']

        # glicko
        self.glicko = glicko_set['initial']
        self.RD = glicko_set['RD']
        self.vol = glicko_set['vol']

        # combo
        self.combo = self.prior
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
        return

    def add_loss(self):
        self.losses += 1
        return

    def add_ties(self):
        self.ties += 1
        return


# end
