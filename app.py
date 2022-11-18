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

#elengos gia to an o user exei eisagei swsto uid
check = 0
while check ==0:
    users_check = scan(es,
    #insert the index that you want data from
        index="users",
        preserve_order=True,
        query={"query": {"match": {"uid" : user }}},
    )

    usr = list(users_check)

    if usr:
        print('User verified. ')
        check = 1
    else:
        print('User does not exist')
        user = input("Write your UID:  ")



#pairnoume ta sxetika vivlia
results_books = scan(es,
    #insert the index that you want data from
    index="books",
    preserve_order=True,
    query={"query": {"match": {"book_title" : search_topic }}},
)

#metatroph to 'generator' object se list gia na einai prospelasimo
books_list = list(results_books)
#print(books_list[1]['_score'])


#printarei ta x pio sxetika vivlia pou vrike
x=0
for book in books_list:
    #change the x for how many data rows you want
    if x<100000:
        
        print(x+1,")", book['_score'], book['_source']['isbn'], book['_source']['book_title'])
        x=x+1
    else:
        break    



#psaxnoyme ti rating exei kanei o xrhsths sta sxetika vivlia poy proekupsan
ratings_full = []
for y in range (len(books_list)):
    isbn =books_list[y]['_source']['isbn']
    
    rating = scan(es,
        #insert the index that you want data from
        index="ratings",
        preserve_order=True,
        query={"query": {"match": {"isbn" : books_list[y]['_source']['isbn'] }, }},
    )

    rating_changed = list(rating) 

    #to kanoyme ayto gia na mpainoyn ola ta ratings gia kathe isbn
    for x in range(len(rating_changed)):
        data = [rating_changed[x]['_source']['uid'],rating_changed[x]['_source']['isbn'],rating_changed[x]['_source']['rating']]
    
        ratings_full.append(data)
    #print(ratings_full)

'''
#ektuposi full ratings
for x in range(len(ratings_full)):
    print(ratings_full[x])
'''

#ratings gia ta isbn poy tairiazoyn 
print("\n", len(ratings_full) , " ratings made \n")

ratings_final = []
for x in range (len(ratings_full)):
    if (ratings_full[x][0] == user ):
        ratings_final.append(ratings_full[x])
        print("added ", x)

#ektuposi final ratings tou xrhsth poy mas endiaferei
if ratings_final:
    for x in range(len(ratings_final)):
        print(ratings_final[x])
else:
    print("\nUser has no recorded ratings for the relative books")        










#BASIKA PROVLIMATA AYTI TIN STIGMH

#na katharistei h lista ratings_final filtrarontas tin analoga me to uid poy mas edose o xrhsths apo thn arxh