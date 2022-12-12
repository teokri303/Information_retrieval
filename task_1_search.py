from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import scan
import pandas as pd
import numpy as np
import time
import csv

ENDPOINT = "http://localhost:9200"
es = Elasticsearch(hosts=ENDPOINT)

#upload code
""" 
To kratame giati etsi fortwsame ta arxeia wste na to deiksoyme sthn anafora

with open("BX-Books.csv") as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index="books")

with open("BX-Users.csv") as x:
    reader = csv.DictReader(x)
    helpers.bulk(es, reader, index="users")

with open("BX-Book-Ratings.csv") as y:
    reader = csv.DictReader(y)
    helpers.bulk(es, reader, index="ratings")
    """


search_topic = input("\nWrite what book do you want to search: ")
user = input("Write your UID:  ")

#elegxos gia to an o user exei eisagei swsto uid
check = 0
while check ==0:
    users_check = scan(es,
    #insert the index that you want data from
        index="users",
        preserve_order=True,
        query={"query": {"match": {"uid" :user}}},
    )

    usr = list(users_check)

    if usr:
        print('User verified. ')
        check = 1
    else:
        print('User does not exist')
        user = input("Write your UID:  ")


start = time.time()

#pairnoume ta sxetika me to alfarithmitiko pou edose o xristis vivlia 
books_final=[]
books_query_results = scan(es,
    #insert the index that you want data from
    index="books",
    preserve_order=True,
    query={"query": {"match": {"book_title" : search_topic }}},
)

#metatroph to 'generator' object se list gia na einai prospelasimo pio eukola
books_mid = list(books_query_results)

#eisagogi stin lista books_final olon ton aparaititon vivliwn
for x in range(len(books_mid)):
        data = [books_mid[x]['_score'], books_mid[x]['_source']['isbn'], books_mid[x]['_source']['book_title']]
    
        books_final.append(data)
'''
#ektuposi twn sxetikwn vivliwn
for x in range(len(books_final)):
        print(x+1, ")", books_final[x][0], books_final[x][1], books_final[x][2])

'''


#psaxnoyme ti rating exei kanei o xrhsths sta sxetika vivlia poy proekupsan
ratings_final = []
for y in range (len(books_final)):
    isbn =books_final[y][1]
    
    #pairnoume ola ta rating poy exoun ginei gia ta sxetika vivlia
    ratings_query_results = scan(es,
        index="ratings",
        preserve_order=True,
        query={"query": {"match": {"isbn" : isbn }, }},
    )

    #metatroph to 'generator' object se list gia na einai prospelasimo pio eukola
    ratings_mid = list(ratings_query_results) 

    #eisagogi stin lista ratings final ton aparaition stoixeiwn
    for x in range(len(ratings_mid)):
        data = [ratings_mid[x]['_source']['uid'],ratings_mid[x]['_source']['isbn'],ratings_mid[x]['_source']['rating']]
    
        ratings_final.append(data)


#ektuposi final ratings (ratings olwn twn vivliwn )
for x in range(len(ratings_final)):
    print(ratings_final[x])


#elegxos gia to an o user exei kanei ratings gia ta sxetika vivlia
user_ratings = []
for x in range (len(ratings_final)):
    if (ratings_final[x][0] == user ):
        user_ratings.append(ratings_final[x])
        print("added ", x)

end = time.time()

      

#Sundiasmos metrikis omoiotitas elasticsearch me to rating ton xrhstwn.
if user_ratings:
    for x in range(len(books_final)):
        for y in range(len(user_ratings)):
            if books_final[x][1] == user_ratings[y][1]:
                books_final[x][1] = books_final[x][1] + user_ratings[y][2]
                print("SCORE CHANGED")

    books_final.sort(reverse=True)
    #EKTUPOSI TELIKON VIVLIWN ME XRISTI POY EXEI KANEI RATING
    print("\nThe top 10% most relevant books for your search are:\n ")
    for x in range(round(len(books_final)/10)):
        print(x+1,')',books_final[x])            
else:
    books_final.sort(reverse=True)
    #EKTUPOSI TELIKON VIVLIWN ME XRISTI POY DEN EXEI KANEI RATING
    print("\nThe top 10% most relevant books for your search are:\n ")
    for x in range(round(len(books_final)/10)):
        print(x+1,')', books_final[x])               




#EKTYPOSEIS TELIKES 
print('\n')
print('--',len(books_final),"Relevant books found.")    
print('--',len(ratings_final) , " Ratings made for these books.") 

#ektuposi final ratings tou xrhsth poy mas endiaferei
if user_ratings:
    for x in range(len(user_ratings)):
        print(user_ratings[x])

    print("User has", len(user_ratings), "recorded ratings for these books.")    
else:
    print("-- User has no recorded ratings for the relevant books.\n\n")  

print('-- We suggest', round(len(books_final)/10), ' (10 precent of all) highest scored books for your search. \n')

print("The execution time for the program is :", (end-start), "seconds\n")    




#TO DO

# Sto telos na emfanizei mono ta 50-100 kalutera tairiasmata kai oxi to 10%
# Na mpei deutero field sthn arxiki anzitisi na exei mesa kai to summary 

