import numpy as np
import pandas as pd

from settings import *
from player import Player
from game import Game

def create_players(league_size):

    players = []
    for p in range(league_size):
        player = Player()
        players.append(player)

    return players

def run_season():

    # import season settings
    league_size = league_set['size']

    # create players
    players = create_players(league_size)

    # simulate one matchup
    game = Game(players[0], players[1])
    print("ELOS")
    print(players[0].elo)
    print(players[1].elo)
    print("Priors")
    print(players[0].prior)
    print(players[1].prior)
    game.play_game()


    return


if __name__ == "__main__":

    run_season()
