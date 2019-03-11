import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

# df = pd.read_csv('elok.csv')
df = pd.read_csv('Error_Analysis.csv')

# plt.plot(df['MOV K'],df['MOV Error'], 'r', label="MOV")
plt.plot(df.Week,df.WL, 'k', label="Win-Loss")
plt.plot(df.Week,df.WLM, 'c', label="Win-Loss Margin")
plt.plot(df.Week,df.Elo, 'r', label="Elo")
# plt.plot(df.Week,df.Prior, 'c', label="Prior")
plt.plot(df.Week,df.MOV, 'b', label="Margin of Victory")
# plt.plot(df.Week,df.Glicko, 'y', label="Glicko")
# plt.plot(df.Week,df.Combo, 'k', label="Combo")

plt.legend()
plt.xlabel("Number of Games")
plt.ylabel("Season Error")
plt.show()















# end
