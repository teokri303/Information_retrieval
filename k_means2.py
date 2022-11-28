import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import plotly.express as exp

data = pd.read_csv('BX-Users.csv')


#---katharismos tou column location gia na meinei mono h xwra---
for x in range(len(data)):
    my_str = data.loc[x,"location"]
    new_val= my_str[my_str.rfind(','):]
    data.loc[x,"location"] = new_val[1:len(new_val)]
    # clear people above 110 age
    if data.loc[x,"age"] >110:
        data.drop(x,axis=0,inplace=True)

ages = data.age.value_counts()
#print(countries)


#---katharismos twn countries kathws uphrxan mesa mi uparktes xwres.---
unique_countries = data['location'].unique()
#arxikos arithmos xwrwn
print("Xwres prin to katharisma: ", len(unique_countries))

for country in unique_countries:
    if len(data[data['location'] == country]) < 15 :
        #print(country, "with entries ", len(data[data['location'] == country]), "DROPPED")
        data.drop(data.loc[data['location'] == country].index, inplace = True) 


unique_countries = data['location'].unique()
print("Xwres meta to katharisma: ", len(unique_countries))
print(unique_countries)

#prepei an vrethei pos ginetai na kano cluster analoga tin xora 
# i toulaxiston na kano ena plot gia hlikies kai xwres

'''
plt.figure(figsize=(9,25))
ax = sns.barplot(x="age", y="Country",
                 data=data, palette="tab20c",
                 linewidth = 1)
for i,j in enumerate(data["age"]):
    ax.text(.5, i, j, weight="bold", color = 'black', fontsize =10)
plt.title("Population of each country in 2020")
ax.set_xlabel(xlabel = 'Population in Billion', fontsize = 10)
ax.set_ylabel(ylabel = 'Countries', fontsize = 10)
plt.show()


'''




'''
kmeans = KMeans(5)
kmeans.fit(data.iloc[:,1:])

'''


'''
sns.set_style("darkgrid")
plt.figure(figsize=(20,20))
sns.barplot(x=countries.index, y=countries.values)
plt.show()

sns.set_style("darkgrid")
plt.figure(figsize=(10,4))
sns.barplot(x=ages.index, y=ages.values)
plt.show()


plt.figure(figsize=(20,20))
plt.title("Ages Frequency")
sns.axes_style("dark")
sns.violinplot(y=data["age"])
plt.show()
'''


print(data.head())