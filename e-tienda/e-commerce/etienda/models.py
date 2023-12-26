# Author: Alejandro Vialard Santana
from pydantic import BaseModel, FilePath, Field
from typing import Any
from django.db import models
from .database import connect_to_mongo
from pprint import pprint
from django.conf import settings
from ninja import UploadedFile
import os
import uuid
from bson import ObjectId
import pathlib

products_collection = connect_to_mongo().products

def convert_mongodb_docs(documents):
    converted_docs = []
    for doc in documents:
        doc['id'] = str(doc['_id'])
        del doc['_id']
        converted_docs.append(doc)
    return converted_docs

def save_image_and_get_path(image: UploadedFile) -> str:
    extension = os.path.splitext(image.name)[1]
    random_name = f"{uuid.uuid4()}{extension}"

    full_image_path = os.path.join(settings.MEDIA_ROOT, 'imagenes', random_name)
    relative_image_path = os.path.join('media', 'imagenes', random_name)

    with open(full_image_path, 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)

    return relative_image_path


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

class ProductManager():

    def add_product_to_collection(data):
        product = {
            "title": data['title'],
            "price": data['price'],
            "description": data['description'],
            "category": data['category']
        }

        if 'image' in data:
            if isinstance(data['image'], UploadedFile):
                image_path = save_image_and_get_path(data['image'])
                product["image"] = image_path
            else:
                product["image"] = data['image']

        products_collection.insert_one(product)

    def get_product_by_id(product_id):
        product = products_collection.find_one({'_id': ObjectId(product_id)})
        if product:
            return convert_mongodb_docs([product])
        return None

    def update_product(product_id, updated_data):
        product = products_collection.find_one({'_id': ObjectId(product_id)})
        if not product:
            return None

        update_data = {'$set': updated_data}
        products_collection.update_one({'_id': ObjectId(product_id)}, update_data)
        return ProductManager.get_product_by_id(product_id)

    def delete_product(product_id):
        product = products_collection.find_one({'_id': ObjectId(product_id)})
        if not product:
            return False, "Product not found"

        if product.get("image"):
            image_path = product.get("image")
            if os.path.exists(image_path):
                os.remove(image_path)

        products_collection.delete_one({'_id': ObjectId(product_id)})
        return True, "Product deleted"

    def list_products_paginated(page, page_size):
        products = products_collection.find().skip(page * page_size).limit(page_size)
        return convert_mongodb_docs(products)

    def print_products_in_query(query):
        for product in query:
            pprint(product)
            print('----------------------')
    
    def get_products_in_price_range_by_category(category, min_price, max_price):
        query = {
            'category': category,
            'price': {
                '$gte': min_price,
                '$lte': max_price
            }
        }
        products = products_collection.find(query).sort('price', 1)
        return convert_mongodb_docs(products)
    
    def get_products_with_keyword_in_description(keyword):
        query = {
            'description': {
                '$regex': keyword,
                '$options': 'i'
            }
        }
        products = products_collection.find(query)
        return convert_mongodb_docs(products)
    
    def get_products_with_rating_above(rating):
        query = {
            'rating.rate': {
                '$gt': rating
            }
        }
        products = products_collection.find(query)
        return convert_mongodb_docs(products)
    
    def get_men_cloting_sorted_by_rating():
        query = {
            'category': 'men\'s clothing'
        }
        products = products_collection.find(query).sort('rating.rate', -1)
        return convert_mongodb_docs(products)
    
    def get_total_revenue():
        query = [
            {
                '$group': {
                    '_id': None,
                    'total': {
                        '$sum': '$price'
                    }
                }
            }
        ]
        return products_collection.aggregate(query)
    
    def get_total_revenue_by_category():
        query = [
            {
                '$group': {
                    '_id': '$category',
                    'total': {
                        '$sum': '$price'
                    }
                }
            }
        ]
        return products_collection.aggregate(query)
    
    def get_products_by_category(category):
        query = {
            'category': category
        }
        products = products_collection.find(query)
        return convert_mongodb_docs(products)
    
    def get_products_with_keyword_in_name(keyword):
        query = {
            'title': {
                '$regex': keyword,
                '$options': 'i'
            }
        }
        products = products_collection.find(query)
        return convert_mongodb_docs(products)
    
    def get_12_random_products():
        query = [
            {
                '$sample': {
                    'size': 12
                }
            }
        ]
        products = products_collection.aggregate(query)
        return convert_mongodb_docs(products)

    def get_all_products():
        products = products_collection.find()
        return convert_mongodb_docs(products)