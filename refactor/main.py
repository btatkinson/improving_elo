import numpy as np
import pandas as pd
import sys
import itertools
import math

from helpers import *
from settings import *

sys.path.insert(0, './classes')
from team import Team
from elo import Elo
from glicko import Glicko

from rpy2.robjects.packages import importr
from tqdm import tqdm
from trueskill import *

# define trueskill environment
ts_env = TrueSkill(mu=trueskill_set['mu'],
                    sigma=trueskill_set['sigma'],
                    beta=trueskill_set['beta'],
                    tau=trueskill_set['tau'],
                    draw_probability=trueskill_set['draw_probability'])
ts_env.make_as_global()

# load R package PlayerRatings
base = importr('base')
utils = importr('utils')
## only need to install once ##
# utils.install_packages('PlayerRatings')
# utils.chooseCRANmirror(ind=65)
pyPR = importr('PlayerRatings')

# select rating systems
## doesn't work right now ##
# rtg_sys = {
# 'Log5':True,
# 'Elo':True,
# 'Improved_Elo':True,
# 'Glicko':True,
# 'TrueSkill':True
# }

# initialize team directory
def init_td(teams):
    team_dir = {}
    for team in teams:
        team_dir[team] = Team(team)
    return team_dir

# main func
def test_systems():
    # load season data
    sdf = pd.read_csv('./data/SeasonResults.csv')

    # separate data into individual seasons
    seasons = list(sdf.Season.unique())

    # set how long before glicko updates
    g_resolve = glicko_set['resolve_time']

    # track error per season
    sea_error = []
    wkbywk_err = None
    for season in tqdm(seasons):
        sea_df = sdf.loc[sdf.Season==season]

        # sort in order
        sea_df = sea_df.sort_values(by='DayNum')
        sea_df = sea_df[['Season','DayNum','WTeam','WScore','LTeam','LScore']]

        # get list of teams in season
        wteams = list(sea_df.WTeam.unique())
        lteams = list(sea_df.LTeam.unique())
        teams = list(set((wteams + lteams)))

        # create team directory to track error
        team_dir = init_td(teams)

        # init classes
        elo = Elo()
        glicko = Glicko()

        # track error per week
        week_err = []
        wk_l5err = wk_eloerr = wk_ieloerr = wk_gerr = wk_tserr = 0
        wk_gp = 0
        wk_thres = 7
        wk_cnt = 0

        # iterate games
        for index, row in sea_df.iterrows():
            t1 = row['WTeam']
            t2 = row['LTeam']
            team1 = team_dir[t1]
            team2 = team_dir[t2]

            # set max number of games for testing
            # if (team1.gp > 11):
            #     continue
            # if (team2.gp > 11):
            #     continue

            # tracking error by week, so check if it's a new week
            day_num = row['DayNum']
            if day_num > wk_thres:
                # it's a new week
                # add end date of next week
                wk_thres += 7
                # ignore weeks that don't have games
                if wk_gp > 0:
                    wk_l5err /= wk_gp
                    wk_eloerr /= wk_gp
                    wk_ieloerr /= wk_gp
                    wk_gerr /= wk_gp
                    wk_tserr /= wk_gp
                    week_err.append([season,wk_cnt,wk_l5err,wk_eloerr,wk_ieloerr,wk_gerr,wk_tserr])
                wk_cnt += 1
                wk_l5err = wk_eloerr = wk_ieloerr = wk_gerr = wk_serr = 0
                wk_gp = 0

            # track games played this week
            wk_gp += 1

            margin = row['WScore'] - row['LScore']

            # get expected outcome for each system
            log5_expect = l5_x(team1.wl, team2.wl)
            elo_expect = elo.x(team1.elo, team2.elo)
            ielo_expect = elo.x(team1.ielo, team2.ielo)
            ts_expect = ts_win_prob([team1.tskill], [team2.tskill])

            # special steps for glicko expectation
            mu, phi = glicko.scale_down(team1.glicko, team1.g_phi)
            mu2, phi2 = glicko.scale_down(team2.glicko, team2.g_phi)
            impact = glicko.reduce_impact(phi2)
            glicko_expect = glicko.get_expected(mu, mu2, impact)

            # update error
            if log5_expect == 0:
                log5_expect += .001
            expects = [log5_expect, elo_expect, ielo_expect, glicko_expect, ts_expect]
            t1_errors = calc_error(expects, 1)
            t2_errors = t1_errors
            team1.update_errors(t1_errors)
            team2.update_errors(t2_errors)

            # update week error
            wk_l5err += t1_errors[0]
            wk_eloerr += t1_errors[1]
            wk_ieloerr += t1_errors[2]
            wk_gerr += t1_errors[3]
            wk_tserr += t1_errors[4]

            ## update ratings ##

            # elo
            elo_delta = elo.get_delta(elo_expect)
            t1_ielo_delta, t2_ielo_delta = elo.get_ielo_delta(ielo_expect, margin, team1, team2)

            team1.update_rating("elo", elo_delta)
            team1.update_rating("ielo", t1_ielo_delta)

            team2.update_rating("elo", -elo_delta)
            team2.update_rating("ielo", t2_ielo_delta)

            team1.update_ts(team2.tskill, "won")
            team2.update_ts(team1.tskill, "lost")

            # log5
            team1.add_win()
            team2.add_loss()

            # glicko (second arg is win or loss)
            team1.add_glicko_opp(team2, 1)
            team2.add_glicko_opp(team1, 0)

            # check if time to resolve
            if team1.gp % g_resolve == 0:
                team1 = glicko.update(team1)
            if team2.gp % g_resolve == 0:
                team2 = glicko.update(team2)



            team_dir[t1] = team1
            team_dir[t2] = team2

        # add week_err df to season trackers
        week_err = pd.DataFrame(week_err,columns=['Season','Week','Log5','Elo','IElo','Glicko','TS'])
        if wkbywk_err is None:
            wkbywk_err = week_err
        else:
            wkbywk_err = pd.concat([wkbywk_err,week_err])

        # find total error in season
        sea_gp = 0
        sea_l5err = 0
        sea_eloerr = 0
        sea_ieloerr = 0
        sea_gerr = 0
        sea_tserr = 0
        for team in team_dir.values():
            sea_gp += team.gp
            sea_l5err += team.l5err
            sea_eloerr += team.eloerr
            sea_ieloerr += team.ieloerr
            sea_gerr += team.glickoerr
            sea_tserr += team.tserr
        sea_l5err /= sea_gp
        sea_eloerr /= sea_gp
        sea_ieloerr /= sea_gp
        sea_gerr /= sea_gp
        sea_tserr /= sea_gp

        sea_error.append([season,sea_l5err,sea_eloerr,sea_ieloerr,sea_gerr,sea_tserr])

    final_table = pd.DataFrame(sea_error, columns=['Season','Log5','Elo','IElo','Glicko','TS'])
    print(final_table)
    print(final_table.mean())

    wkbywk = pd.DataFrame(wkbywk_err, columns=['Season','Week','Log5','Elo','IElo','Glicko','TS'])
    print(wkbywk.groupby('Week').mean())
    return

if __name__ == "__main__":

    test_systems()



# end
