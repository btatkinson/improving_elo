import numpy as np
import pandas as pd

import rpy2.robjects as ro
from rpy2.robjects.packages import importr
# tzlocal = importr('tzlocal')
from rpy2.robjects import pandas2ri

from rpy2.robjects.conversion import localconverter

base = importr('base')

utils = importr('utils')


## only need to install once ##
# utils.install_packages('PlayerRatings')
# utils.chooseCRANmirror(ind=65)

pyPR = importr('PlayerRatings')

pd_df = pd.DataFrame({
                        'Time Period': [1,1,1],
                        'Player 1': [1,2,3],
                        'Player 2': [2,3,1],
                        'Result': [1,0,0]
                    })
print(pd_df)

with localconverter(ro.default_converter + pandas2ri.converter):
  r_from_pd_df = ro.conversion.py2rpy(pd_df)

print(r_from_pd_df)

sobj = pyPR.steph(r_from_pd_df, cval=8, hval=8)


#
