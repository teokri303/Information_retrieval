import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from keras.models import Sequential
from keras.layers import Dense

# pairnoume ta aparaitita arxeia 
data = pd.read_csv('Updated-Ratings.csv')
books = pd.read_csv('BX-Books.csv')
clust_1 = pd.read_csv('Clust_1.csv')
clust_2 = pd.read_csv('Clust_2.csv')
clust_3 = pd.read_csv('Clust_3.csv')

zero_ratings = data[data['rating'] == 0]

c1_uids = list(set(clust_1.uid).intersection(set(data.uid)))
c2_uids = list(set(clust_2.uid).intersection(set(data.uid)))
c3_uids = list(set(clust_3.uid).intersection(set(data.uid)))


# diaxorizoume ta ratings pou exoume analoga me to cluster twn users pou tis ekanan
c1_ratings = data[data.uid.isin(c1_uids)]
c2_ratings = data[data.uid.isin(c2_uids)]
c3_ratings = data[data.uid.isin(c3_uids)]

#print(len(c1_ratings))
#print(len(c2_ratings))
#print(len(c3_ratings))

# apo edw argotera tha to automatopoihsoyme gia na ginetai mia fora gia ola.
clusters = [c1_ratings, c2_ratings, c3_ratings]

for cluster in clusters:
    # diaxwrizoume tis vathmologies tou kathe cluster se zero kai non_zero
    zero_ratings_clust = cluster[cluster['rating'] == 0]
    non_zero_ratings_clust = cluster[cluster['rating'] != 0]

    # prosthetoume sta dedomena ta summaries gia to kathe vivlio poy exei vathmologithei sto cluster
    sum1_non_zero = pd.merge(non_zero_ratings_clust, books, how='inner', on='isbn')
    sum1_zero = pd.merge(zero_ratings_clust, books, how='inner', on='isbn')

    # ksexwriszoume ta summaries se listes wste na einai etoima gia to vectorization
    sums = sum1_non_zero.summary.values.tolist()
    zero_sums = sum1_zero.summary.values.tolist()

    #makings vectors
    # gia ta non zero summaries pou tha einai to X_train
    print('Gia to trehon Cluster exoume: ' )

    model_vect = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    X_train = model_vect.encode(sums)
    print('Non zero ratings tou cluster: ', len(X_train))

    # oi vathmologies twn non zero books pou tha perasoun sto model mazi me ta summaries
    y_train = sum1_non_zero.rating.values.tolist()

    # gia ta zero summaries pou tha einai to X_test
    model_vect = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    X_test = model_vect.encode(zero_sums)
    print('Zero ratings tou cluster: ', len(X_test))

    # metatroph se np arrays giati allios den mporoun na mpoun sto keras model
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    X_test = np.array(X_test)

    #creating layers
    model = Sequential()
    model.add(Dense(384, input_shape = (384,)))
    #model.add(Dropout(0.3))
    model.add(Dense(192, activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(96, activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(1, activation='relu'))


    # model compile apairaitito prin tin xrhsh tou model 
    model.compile(optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy'])


    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    # etoimasia twn ratings gia eisagwgh
    y_pred = np.array(y_pred)
    values = y_pred.flatten()
    values = np.round(values, 0)

    zero_ratings_clust['rating'] = values


    # eidagwgh twn provlepsewn sta arxika ratings kai antikatastash twn 0 
    data.update(zero_ratings_clust)

    print(len(data))
    zero_ratings = data[data['rating'] == 0]
    print('OLA TA ZERO RATINGS meta tin prosthiki tis provlepsis: ' , len(zero_ratings) )

