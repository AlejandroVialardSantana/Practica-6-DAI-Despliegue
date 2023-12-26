# Seed.py
# Author: Alejandro Vialard Santana
from pydantic import BaseModel, FilePath, Field, ValidationError, EmailStr
import pathlib
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests
import os

class Rating(BaseModel):
	rate: float = Field(ge=0., le=5.)
	count: int = Field(ge=1)

class Product(BaseModel):
	_id: Any
	name: str
	price: float
	description: str
	category: str
	image: FilePath | None
	rating: Rating

class Buy(BaseModel):
	_id: Any
	user: EmailStr
	date: datetime
	products: list

def get_products(api):
	response = requests.get(api)
	return response.json()
	
data = { 
	'name': "MBJ Women's Solid Short Sleeve Boat Neck V ", 
	'price': 9.85, 
	'description': '95% RAYON 5% SPANDEX, Made in USA or Imported, Do Not Bleach, Lightweight fabric with great stretch for comfort, Ribbed on sleeves and neckline / Double stitching on bottom hem', 'category': "women's clothing", 
	'category': "women's clothing",
	'image': None, 
	'rating': {'rate': 4.9, 'count': 130}
}
 
product = Product(**data)

try:
    product = Product(**data)
except ValidationError as e:
    print(e.errors())

# print(product.description)
# pprint(product.model_dump()) # Objeto -> python dict

def connect_to_mongo():
	client = MongoClient('mongo', 27017)
	db = client.ecommerce # Database
	return db

products_collection = connect_to_mongo().products # Products Collection

def insert_one_product(product):
	products_collection.insert_one(product.model_dump())
      
# insert_one_product(product)

products_list_ids = []

def get_products_by_id_and_insert_in_list():
	for product in products_collection.find():
		pprint(product)
		print('----------------------')
		print(product.get('_id'))
		products_list_ids.append(product.get('_id'))

# get_products_by_id_and_insert_in_list()	
# print(products_list_ids)

new_buy = {
	'user': 'pepe@gmail.com',
	'date': datetime.now(),
	'products': products_list_ids
}

buy = Buy(**new_buy)

# pprint(buy.model_dump())

buys_collection = connect_to_mongo().buys

def insert_one_buy(buy):
	buys_collection.insert_one(buy.model_dump())

# insert_one_buy(buy)

def print_buys():
	for buy in buys_collection.find():
		pprint(buy)
		print('----------------------')

# print_buys()

def insert_products_from_api(api):
    for product in get_products(api):
        pprint(product)
        print('----------------------')
        
        # Suponiendo que cada producto tiene un campo 'id' único
        product_id = product.get('id')
        
        if product.get('image') and 'https://fakestoreapi.com/img/' in product['image']:
            image_url = product['image']
            image_name = os.path.basename(image_url)
            image_path = os.path.join('media/imagenes', image_name)

            response = requests.get(image_url)
            with open(image_path, 'wb') as f:
                f.write(response.content)

            product['image'] = image_path
        
        # Actualizar el producto si ya existe basándose en el 'id', de lo contrario, insertarlo
        products_collection.update_one({'id': product_id}, {'$set': product}, upsert=True)



def delete_products():
    products_to_delete = list(products_collection.find())

    products_collection.delete_many({})

    for product in products_to_delete:
        image_path = product.get('image')
        if image_path:
            try:
                os.remove(image_path)
                print(f"Imagen eliminada: {image_path}")
            except FileNotFoundError:
                print(f"La imagen no existe: {image_path}")


def delete_buys():
	buys_collection.delete_many({})

# insert_one_product(product)

# insert_products_from_api('https://fakestoreapi.com/products')
# pprint(products_collection.count_documents({}))
# pprint(products_collection.find_one({}))
# pprint(buys_collection.count_documents({}))
# pprint(buys_collection.find_one({}))

# delete_products()
# delete_buys()