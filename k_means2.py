import pandas as pd
import numpy as np
import random as rd
import matplotlib.pyplot as plt

data = pd.read_csv('BX-Users.csv')

# katharismow tou column location gia na meinei mono h xwra
for x in range(len(data)):
    my_str = data.loc[x,"location"]
    new_val= my_str[my_str.rfind(','):]
    data.loc[x,"location"] = new_val[1:len(new_val)]





data.head()