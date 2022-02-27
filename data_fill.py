import json
import pymongo

# connect to MongoDB
connection_string = 'mongodb://127.0.0.1:27017/store'
client = pymongo.MongoClient(connection_string)

dbname = client['store']
products = dbname['products']

file = open('product_data.json', 'rb')
data = file.read()

json_data = json.loads(data)
print(len(json_data))  # 12491 products

number_of_products = 400

# for i in range(number_of_products):
#     # load 100 products
#     product = json_data[i]
#     product_data = {
#         "name": product.get('name'),
#         "images": product.get('images').split('~'),
#         "description": product.get('description'),
#         "price": 5.54 * int(product.get('price')),
#         "brand": product.get('brand'),
#         "currency": "NGN",
#         "in_stock": product.get('in_stock'),
#         "gender": product.get('gender')
#     }
#     products.insert_one(product_data)

# print(products.count())
