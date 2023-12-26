# Author: Alejandro Vialard Santana

from Seed import connect_to_mongo
from pprint import pprint

products_collection = connect_to_mongo().products

def get_products_in_price_range_by_category(category, min_price, max_price):
    query = {
        'category': category,
        'price': {
            '$gte': min_price,
            '$lte': max_price
        }
    }
    return products_collection.find(query).sort('price', 1)

def get_products_with_keyword_in_description(keyword):
    query = {
        'description': {
            '$regex': keyword,
            '$options': 'i'
        }
    }
    return products_collection.find(query)

def get_products_with_rating_above(rating):
    query = {
        'rating.rate': {
            '$gt': rating
        }
    }
    return products_collection.find(query)

def get_men_cloting_sorted_by_rating():
    query = {
        'category': 'men\'s clothing'
    }
    return products_collection.find(query).sort('rating.rate', -1)

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

query_1 = get_products_in_price_range_by_category("electronics", 100, 200)
query_2 = get_products_with_keyword_in_description('pocket')
query_3 = get_products_with_rating_above(4)
query_4 = get_men_cloting_sorted_by_rating()
query_5 = get_total_revenue()
query_6 = get_total_revenue_by_category()

print_products_in_query(query_1)

print_products_in_query(query_2)
 
print_products_in_query(query_3)
 
print_products_in_query(query_4)
 
print_products_in_query(query_5)

print_products_in_query(query_6)