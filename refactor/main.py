import numpy as np
import pandas as pd
import sys

from math import log

sys.path.insert(0, './classes')
from team import Team
from elo import Elo
from glicko import Glicko
from steph import Steph
from settings import *

from tqdm import tqdm

# select rating systems
rtg_sys = {
'Log5':True,
'Elo':True,
'Improved_Elo':True,
'Glicko':True,
'Stephenson':True
}
# adjust parameters of systems in systems/settings

# helper funx
def init_td(teams):
    team_dir = {}
    for team in teams:
        team_dir[team] = Team(team)
    return team_dir

def l5_x(pa, pb):
    if pa == pb:
        return 0.5
    return (pa - (pa * pb))/((pa + pb) - (2 * pa * pb))

def calc_error(expected_array, result):
    if result == 1:
        return [-log(p) for p in expected_array]
    else:
        return [-log(1-p) for p in expected_array]

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

        # sort in order (DayNum inspired by kaggle)
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
        steph = Steph()

        # test glicko
        # team1 = Team(1)
        # t2 = Team(2)
        # t3 = Team(3)
        # t4 = Team(4)
        #
        # team1.glicko = 1500
        # t2.glicko = 1400
        # t3.glicko = 1550
        # t4.glicko = 1700
        #
        # team1.g_phi = 200
        # t2.g_phi = 30
        # t3.g_phi = 100
        # t4.g_phi = 300
        #
        # team1.add_glicko_opp(t2,1)
        # team1.add_glicko_opp(t3,0)
        # team1.add_glicko_opp(t4,0)
        #
        # team1 = glicko.update(team1)
        # print(team1.glicko, team1.g_phi, team1.g_sigma)
        # raise ValueError

        # track error per week
        week_err = []
        wk_l5err = wk_eloerr = wk_ieloerr = wk_gerr = wk_serr = 0
        wk_gp = 0
        wk_thres = 7
        wk_cnt = 0
        # iterate games
        for index, row in sea_df.iterrows():
            t1 = row['WTeam']
            t2 = row['LTeam']
            team1 = team_dir[t1]
            team2 = team_dir[t2]

            # if (team1.gp > 11):
            #     continue
            # if (team2.gp > 11):
            #     continue

            # tracking error by week, so check if it's a new week
            day_num = row['DayNum']
            if day_num > wk_thres:
                # it's a new week
                wk_thres += 7
                if wk_gp > 0:
                    wk_l5err /= wk_gp
                    wk_eloerr /= wk_gp
                    wk_ieloerr /= wk_gp
                    wk_gerr /= wk_gp
                    wk_serr /= wk_gp
                    week_err.append([season,wk_cnt,wk_l5err,wk_eloerr,wk_ieloerr,wk_gerr,wk_serr])
                    wk_cnt += 1
                    wk_l5err = wk_eloerr = wk_ieloerr = wk_gerr = wk_serr = 0
                    wk_gp = 0
            wk_gp += 1

            margin = row['WScore'] - row['LScore']

            # get expected outcome for each system
            log5_expect = l5_x(team1.wl, team2.wl)
            elo_expect = elo.x(team1.elo, team2.elo)
            ielo_expect = elo.x(team1.ielo, team2.ielo)

            glicko_expect = 0.5
            steph_expect = 0.5
            # glicko_expect = glicko.x(team1, team2)
            # steph_expect = steph.x(team1, team2)

            # update error
            if log5_expect == 0:
                log5_expect += .001
            expects = [log5_expect, elo_expect, ielo_expect, glicko_expect, steph_expect]
            t1_errors = calc_error(expects, 1)
            t2_errors = t1_errors
            team1.update_errors(t1_errors)
            team2.update_errors(t2_errors)

            # update week error
            wk_l5err += t1_errors[0]
            wk_eloerr += t1_errors[1]
            wk_ieloerr += t1_errors[2]
            wk_gerr += t1_errors[3]
            wk_serr += t1_errors[4]

            # update ratings

            # elo
            elo_delta = elo.get_delta(elo_expect)
            t1_ielo_delta, t2_ielo_delta = elo.get_ielo_delta(ielo_expect, margin, team1, team2)

            team1.update_rating("elo", elo_delta)
            team1.update_rating("ielo", t1_ielo_delta)

            team2.update_rating("elo", -elo_delta)
            team2.update_rating("ielo", t2_ielo_delta)

            # log5

            team1.add_win()
            team2.add_loss()

            # glicko
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
        week_err = pd.DataFrame(week_err,columns=['Season','Week','Log5','Elo','IElo','Glicko','Steph'])
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
        sea_serr = 0
        for team in team_dir.values():
            sea_gp += team.gp
            sea_l5err += team.l5err
            sea_eloerr += team.eloerr
            sea_ieloerr += team.ieloerr
            sea_gerr += team.glickoerr
            sea_serr += team.stepherr
        sea_l5err /= sea_gp
        sea_eloerr /= sea_gp
        sea_ieloerr /= sea_gp
        sea_gerr /= sea_gp
        sea_serr /= sea_gp

        sea_error.append([season,sea_l5err,sea_eloerr,sea_ieloerr,sea_gerr,sea_serr])

    final_table = pd.DataFrame(sea_error, columns=['Season','Log5','Elo','IElo','Glicko','Steph'])
    print(final_table)
    print(final_table.mean())

    wkbywk = pd.DataFrame(wkbywk_err, columns=['Season','Week','Log5','Elo','IElo','Glicko','Steph'])
    print(wkbywk.groupby('Week').mean())
    return

if __name__ == "__main__":

    test_systems()



# end
