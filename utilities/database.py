import os

import pymongo

connection_string = os.environ.get('MONGO_URI')
client = pymongo.MongoClient(connection_string)
dbname = client['store']
categories = dbname['categories']