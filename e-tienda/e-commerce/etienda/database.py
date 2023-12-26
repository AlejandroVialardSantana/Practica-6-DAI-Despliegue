from pymongo import MongoClient

def connect_to_mongo():
    client = MongoClient('mongo', 27017)
    db = client.ecommerce
    return db