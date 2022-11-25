import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('BX-Users.csv')


# katharismow tou column location gia na meinei mono h xwra
print("Start of location and age filtering. \n")
for x in range(len(data)):
    my_str = data.loc[x,"location"]
    new_val= my_str[my_str.rfind(','):]
    data.loc[x,"location"] = new_val[1:len(new_val)]
    # clear people above 110 age
    if data.loc[x,"age"] >110:
        data.drop(x,axis=0,inplace=True)

# xreiazetai epipleon filter gia lathos grammenes xorew
print("Values count. \n")
countries = data.location.value_counts()
ages = data.age.value_counts()



'''
print("Plots making. \n")
sns.set_style("darkgrid")
plt.figure(figsize=(10,20))
sns.barplot(x=countries.index, y=countries.values)
plt.show()

sns.set_style("darkgrid")
plt.figure(figsize=(10,4))
sns.barplot(x=ages.index, y=ages.values)
plt.show()


plt.figure(figsize=(10,5))
plt.title("Ages Frequency")
sns.axes_style("dark")
sns.violinplot(y=data["age"])
plt.show()


data.head()'''