import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_blobs
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


def makePlot(number): 

    for x in range(number):
        country = unique_countries[x]
        age18_25 = data[data['location'] == country]['age'][(data[data['location'] == country]['age'] <= 25) & (data[data['location'] == country]['age'] >= 18)]
        age26_35 = data[data['location'] == country]['age'][(data[data['location'] == country]['age'] <= 35) & (data[data['location'] == country]['age'] >= 26)]
        age36_45 = data[data['location'] == country]['age'][(data[data['location'] == country]['age'] <= 45) & (data[data['location'] == country]['age'] >= 36)]
        age46_55 = data[data['location'] == country]['age'][(data[data['location'] == country]['age'] <= 55) & (data[data['location'] == country]['age'] >= 46)]
        age55above = data[data['location'] == country]['age'][data[data['location'] == country]['age'] >= 56]

        x = ["18-25","26-35","36-45","46-55","55+"]
        y = [len(age18_25.values),len(age26_35.values),len(age36_45.values),len(age46_55.values),len(age55above.values)]

        plt.figure(figsize=(15,6))
        sns.barplot(x=x, y=y, palette="rocket")
        plt.title(country)
        plt.xlabel("Age")
        plt.ylabel("COUNT OF PEOPLE")
        plt.show()  

#makePlot(5)


each_country = data.loc[data['location'] == ' usa']
each_country = each_country.dropna()
#each_country['age'].values.reshape(1,-1)


#print(each_country.iloc[5]['location'])
each_country['location'] = each_country['location'].replace(each_country.iloc[0]['location'], 1)



print(each_country)

each_country.info()
#edw ginetai kanonikopoisi
scaler = StandardScaler()
scaled_features = scaler.fit_transform([each_country['age']])











