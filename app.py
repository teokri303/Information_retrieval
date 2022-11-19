from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import scan
import pandas as pd
import numpy as np
import sys
import json
import csv


ENDPOINT = "http://localhost:9200"
es = Elasticsearch(hosts=ENDPOINT)

""" 
To kratame giati etsi fortwsame ta arxeia wste na to deiksoyme sthn anafora

with open("BX-Books.csv") as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index="books")

with open("BX-Users.csv") as x:
    reader = csv.DictReader(x)
    helpers.bulk(es, reader, index="users")\

with open("BX-Book-Ratings.csv") as y:
    reader = csv.DictReader(y)
    helpers.bulk(es, reader, index="ratings")
    """

"""
logika tha fugei auto 
def get_data_from_elastic():
    # query: The elasticsearch query.
    query = {
        "query": {
            "match_all": {}
            
        }
    }
    # Scan function to get all the data.
    rel = scan(client=es,
               query=query,
               scroll='1m',
               index='ratings',
               raise_on_error=True,
               preserve_order=False,
               clear_scroll=True)
    # Keep response in a list.
    result = list(rel)
    temp = []
    
    
    # We need only '_source', which has all the fields required.
    # This elimantes the elasticsearch metdata like _id, _type, _index.
    
    for hit in result:
        temp.append(hit['_source'])
    # Create a dataframe.
    df = pd.DataFrame(temp)
    return df


df = get_data_from_elastic()


print(df.head())

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


#ektuposi final ratings
for x in range(len(ratings_final)):
    print(ratings_final[x])

print('\n')
print('--',len(books_final),"Relevant books found.")    
print('--',len(ratings_final) , " Ratings made for these books.")  


#ratings gia ta isbn poy tairiazoyn 
user_ratings = []
for x in range (len(ratings_final)):
    if (ratings_final[x][0] == user ):
        user_ratings.append(ratings_final[x])
        print("added ", x)

#ektuposi final ratings tou xrhsth poy mas endiaferei
if user_ratings:
    for x in range(len(user_ratings)):
        print(user_ratings[x])

    print("User has", len(user_ratings), "recorded ratings for these books.")    
else:
    print("--User has no recorded ratings for the relevant books.\n")        




#ksekiname ton elegxo gia ton orismo twn swstwn score

if user_ratings:
    for x in range(len(books_final)):
        for y in range(len(user_ratings)):
            if books_final[x][1] == user_ratings[y][1]:
                books_final[x][1] = books_final[x][1] + user_ratings[y][2]
                print("SCORE CHANGED")

    books_final.sort(reverse=True)
    for x in range(len(books_final)):
        print(books_final[x])            
else:
    books_final.sort(reverse=True)
    '''
    for x in range(len(books_final)):
        print(books_final[x])               
'''




#μενει απλα να εμφανιζει μονο το 10% με τα καλυτερα

#BASIKA PROVLIMATA AYTI TIN STIGMH

# προβλημα με τα uid απο τα δεδομενα. Πολλα uid υπαρχουν στα ratings αλλα δεν υπαρχουν στους users.
# δεν πετυχαινεις ευκολα user να εχει κανει κριτικες