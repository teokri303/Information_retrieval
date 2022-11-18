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

search_topic = input("Write what book do you want to search: ")
#user = input("Write your UID:  ")

results = scan(es,
    #insert the index that you want data from
    index="books",
    preserve_order=True,
    query={"query": {"match": {"book_title" : search_topic }}},
)




x=0
for item in results:
    #change the x for how many data rows you want
    if x<100:
        #print(item)
        print(item['_score'], item['_source']['isbn'], item['_source']['book_title'])
        x=x+1
    else:
        break    
