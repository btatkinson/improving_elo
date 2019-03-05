import numpy as np
import pandas as pd
import random

class Schedule(object):
    """docstring for Schedule."""
    def __init__(self, players, num_games, skill_gap, day_by_day):
        super(Schedule, self).__init__()
        self.players = players
        self.num_games = num_games
        self.skill_gap = skill_gap
        self.day_by_day = day_by_day

    def create_matchups(self):
        contestants = self.players.copy()
        pairs = []
        random.shuffle(contestants)
        for x in range(int(len(contestants)/2)):
            p1 = contestants.pop()
            p2 = contestants.pop()
            pair = [p1, p2]
            pairs.append(pair)
        return pairs



# end
