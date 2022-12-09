import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as exp

data = pd.read_csv('BX-Users.csv')
ratings = pd.read_csv('BX-Book-Ratings.csv')


#---katharismos tou column location gia na meinei mono h xwra---
for x in range(len(data)):
    my_str = data.loc[x,"location"]
    new_val= my_str[my_str.rfind(','):]
    data.loc[x,"location"] = new_val[1:len(new_val)]
    # clear people above 110 age
    if data.loc[x,"age"] >110 or data.loc[x,"age"] <10:
        data.drop(x,axis=0,inplace=True)

#---katharismos twn countries kathws uphrxan mesa mi uparktes xwres.---
unique_countries = data['location'].unique()
#arxikos arithmos xwrwn
print("Xwres prin to katharisma: ", len(unique_countries))

#---diagrafi twn xwrwn pou emfanizontai ligoteres apo 15 fores kathws opws eidame den einai egkyres
for country in unique_countries:  
    if len(data[data['location'] == country]) < 15 :
        #print(country, "with entries ", len(data[data['location'] == country]), "DROPPED")
        data.drop(data.loc[data['location'] == country].index, inplace = True) 

unique_countries = data['location'].unique()
print("Xwres meta to katharisma: ", len(unique_countries))

#function gia na plottarei tis meses hlikies kathe xwras
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



#vazoume gia kathe xwra ena monadiko arithmo gia na perasei sto model
for country in unique_countries:
    #print(country, np.where(unique_countries == country)[0][0])
    data['location'] = data['location'].replace(country, np.where(unique_countries == country)[0][0])

#dropparoume tis Nan times gia na mporei na mpei sto kmean model
data = data.dropna()


X = np.array(data.loc[:,['location', 'age']])


kmeans = KMeans(init="random",n_clusters=3,n_init=10,max_iter=300,random_state=42)

model = kmeans.fit_predict(X)

# to model einai ta labels gia to pou anikei o kathe user
#print(len(model))


plt.scatter(X[:,0], X[:,1])
plt.scatter(kmeans.cluster_centers_[:, 0], 
            kmeans.cluster_centers_[:, 1], 
            s=20,     # Set centroid size
            c='red')  # Set centroid color
plt.show()
 

# enallagh pali se xwres anti gia arithmous gia na proxwrisoume se diaxwrismo
for country in unique_countries:
    data['location'] = data['location'].replace(np.where(unique_countries == country)[0][0], country) 


data = data.reset_index(drop=True)

#eisagoume neo column sta data me to se poio cluster anikei o kahte user
data['cluster'] = model

# edw ksexwrizoyme tous users me vasi to cluster pou tous anatehike
# isws xreiastei reset index
clust_1 = data[data['cluster'] == 0]
clust_2 = data[data['cluster'] == 1]
clust_3 = data[data['cluster'] == 2]

#print(data.head)

zero_ratings = ratings[ratings['rating'] == 0]
zero_ratings = zero_ratings.reset_index(drop=True)
#zero_ratings.head


non_zero_ratings = ratings[ratings['rating'] != 0]
non_zero_ratings = non_zero_ratings.reset_index(drop=True)


clust_1_users_ratings = pd.DataFrame()
clust_2_users_ratings = pd.DataFrame()
clust_3_users_ratings = pd.DataFrame()

#Kathe dataframe exei tous users tou kathe cluster kai kathe vivlio pou exoun vathmologisei
for x in range(len(non_zero_ratings)):
    if non_zero_ratings.iloc[x]['uid'] in clust_1['uid'].values:
        clust_1_users_ratings = pd.concat([clust_1_users_ratings, non_zero_ratings.iloc[[x]]])

for x in range(len(non_zero_ratings)):
    if non_zero_ratings.iloc[x]['uid'] in clust_2['uid'].values:
        clust_2_users_ratings = pd.concat([clust_2_users_ratings, non_zero_ratings.iloc[[x]]])

for x in range(len(non_zero_ratings)):
    if non_zero_ratings.iloc[x]['uid'] in clust_3['uid'].values:
        clust_3_users_ratings = pd.concat([clust_3_users_ratings, non_zero_ratings.iloc[[x]]])



print(clust_1_users_ratings.head)
#print(clust_2_users_ratings.head)
#print(clust_3_users_ratings.head)


books_rat_clust1 = np.empty((0, 2), int)
books_rat_clust2 = np.empty((0, 2), int)
books_rat_clust3 = np.empty((0, 2), int)



for book in range(len(zero_ratings)):
    
    # etsi pairno me tin seira isbn apo ta zero
    x = zero_ratings.iloc[book]['isbn']

    # elegxei an yparxei to isbn sta non zero
    if x in clust_1_users_ratings['isbn'].values:
        # poses fores uparxei auto to isbn sta non zero
        #clust_1_users_ratings['isbn'].value_counts()[x]
        
        # edw vazo se ena neo dataframe oles tis vathmologies twn allwn users gia to biblio
        ongoing_book_rating=clust_1_users_ratings[clust_1_users_ratings['isbn'] == x]
        # vrisko tin mesi timi giauto to vivlio gia tous user pou to exoun vathmologisei
        mean=ongoing_book_rating['rating'].mean()
        # vazoume sto array to isbn kai dipla ton meso oro twn vathmologiwn
        books_rat_clust1=np.append(books_rat_clust1, np.array([[x, mean]]), axis=0)

    if x in clust_2_users_ratings['isbn'].values:
        
        # edw vazo se ena neo dataframe oles tis vathmologies twn allwn users gia to biblio
        ongoing_book_rating=clust_2_users_ratings[clust_2_users_ratings['isbn'] == x]
        # vrisko tin mesi timi giauto to vivlio gia tous user pou to exoun vathmologisei
        mean=ongoing_book_rating['rating'].mean()
        # vazoume sto array to isbn kai dipla ton meso oro twn vathmologiwn
        books_rat_clust2=np.append(books_rat_clust2, np.array([[x, mean]]), axis=0)

    if x in clust_3_users_ratings['isbn'].values:
      
        # edw vazo se ena neo dataframe oles tis vathmologies twn allwn users gia to biblio
        ongoing_book_rating=clust_3_users_ratings[clust_3_users_ratings['isbn'] == x]
        # vrisko tin mesi timi giauto to vivlio gia tous user pou to exoun vathmologisei
        mean=ongoing_book_rating['rating'].mean()
        # vazoume sto array to isbn kai dipla ton meso oro twn vathmologiwn
        books_rat_clust3=np.append(books_rat_clust3, np.array([[x, mean]]), axis=0)        

