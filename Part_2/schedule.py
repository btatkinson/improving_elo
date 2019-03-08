import numpy as np
import pandas as pd
import random

from settings import *

class Schedule(object):
    """docstring for Schedule."""
    def __init__(self):
        super(Schedule, self).__init__()
        self.weeks = schedule_set['weeks']
        self.ppw = schedule_set['players_per_week']
        self.nudge = schedule_set['daily_nudge']
        self.rating_period = schedule_set['rating_period']

    def create_calendar(self):
        self.calendar = []
        for i in range(self.weeks):
            week = i + 1
            if week % self.rating_period == 0:
                self.calendar.extend(["OFF","OFF","OFF","OFF","OFF","OFF","RATE"])
            else:
                self.calendar.extend(["OFF","OFF","OFF","OFF","OFF","OFF","GAMES"])
        return self.calendar

    def nudge_ratings(self,players):
        adj_players = []
        for player in players:
            direction = random.randint(0,1)
            if direction == 0:
                player.rating += self.nudge
            else:
                player.rating -= self.nudge
            adj_players.append(player)
        return adj_players

    def create_matchups(self,players):
        random.shuffle(players)
        # separate players between those playing and not
        this_week = players[:self.ppw]
        players_off = players[self.ppw:]
        matchups = []
        while len(this_week) > 0:
            p1 = this_week.pop()
            p2 = this_week.pop()
            matchups.append([p1,p2])
        return matchups, players_off





#end
