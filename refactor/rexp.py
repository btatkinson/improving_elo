import numpy as np
import pandas as pd

from rpy2.robjects.packages import importr

base = importr('base')

utils = importr('utils')

## only need to install once ##
# utils.install_packages('PlayerRatings')
# utils.chooseCRANmirror(ind=65)

pyPR = importr('PlayerRatings')

x = []
x.append([1,1,2,1])


sobj = pyPR.steph(x, init=[2200,300], cval=8, hval=8)

print(sobj)


#
