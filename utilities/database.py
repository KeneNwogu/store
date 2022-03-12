import pymongo

connection_string = 'mongodb://127.0.0.1:27017/store'
client = pymongo.MongoClient(connection_string)
dbname = client['store']
categories = dbname['categories']