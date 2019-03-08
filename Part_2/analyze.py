import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

df = pd.read_csv('Error_Analysis.csv')

plt.plot(df.Week,df.WL, 'r', label="Win-Loss")
plt.plot(df.Week,df.WLM, 'b', label="Win-Loss Margin")
plt.plot(df.Week,df.Elo, 'g', label="Elo")
plt.plot(df.Week,df.Prior, 'c', label="Prior")
plt.plot(df.Week,df.MOV, 'm', label="Margin of Victory")
plt.plot(df.Week,df.Glicko, 'y', label="Glicko")
plt.plot(df.Week,df.Combo, 'k', label="Combo")

plt.legend()
plt.show()















# end
