import json
import pymongo
import re

# connect to MongoDB
connection_string = 'mongodb://127.0.0.1:27017/store'
client = pymongo.MongoClient(connection_string)

dbname = client['store']
products = dbname['products']
categories = dbname['categories']

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
# brands = []
# counter = []

# for product in list(products.find()):
#     # tally brand
#     if product.get('brand') not in brands:
#         brands.append(product.get('brand'))
#         counter.append(1)
#     else:
#         index = brands.index(product.get('brand'))
#         counter[index] += 1

keywords = ['Dress', 'T-shirt', 'Bag', 'Jacket', 'Jeans', 'Sportwear', 'Sleeves', 'Shorts',
            'Sneakers', 'Bra']
counter = {}
for product in list(products.find()):
    # tally keywords
    for keyword in keywords:
        # if keyword matches description
        description = product.get('description')

        if re.search(keyword.lower(), description.lower()):
            if counter.get(keyword):
                counter[keyword] += 1
            else:
                counter[keyword] = 1

print(counter)

# for key in counter.keys():
#     data = {
#         "type": "keyword",
#         "keyword": key,
#         "count": counter[key]
#     }
#     categories.insert_one(data)
# print(brands)
# print(counter)

# brand_results = list(zip(brands, counter))
# for result in brand_results:
#     category = {
#         "type": "brand",
#         "brand": result[0],
#         "count": result[1]
#     }
#     categories.insert_one(category)
# print(re.search('bavuiffig', 'Black and grey printed medium trolley bag, secured with a TSA lockOne handle on the top and one on the side, has a trolley with a retractable handle on the top and four corner mounted inline skate wheelsOne main zip compartment, zip lining, two compression straps with click clasps, one zip compartment on the flap with three zip pocketsWarranty: 5 yearsWarranty provided by Brand Owner / Manufacturer'))
print('done')