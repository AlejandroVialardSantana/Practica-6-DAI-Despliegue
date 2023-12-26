from ninja_extra import NinjaExtraAPI, api_controller, http_get
from pydantic import BaseModel as Schema
from ninja import File, UploadedFile
from ninja.security import HttpBearer
from .models import *
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "testtoken":
            return token

api = NinjaExtraAPI(auth=GlobalAuth())
        
class Rate(Schema):
	rate: float
	count: int
	
class ProductSchema(Schema):
	id: str
	title: str
	price: float
	description: str
	category: str
	image: str = None
	rating: Rate
	
class ProductSchemaIn(Schema):
    title: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[Rate] = None
	
class ErrorSchema(Schema):
	message: str

@api.get("/products/paginated", tags=['Productos'])
def list_products(request, page: int = 0, page_size: int = 4):
	products = ProductManager.list_products_paginated(page, page_size)
	logger.info(f"Products listed: {products}")
	return {"ok": "yes", "data": products}

@api.get("/products", tags=['Productos'])
def list_all_products(request):
    products = ProductManager.get_all_products()
    logger.info(f"Products listed: {products}")
    return {"ok": "yes", "data": products}

@api.get("/products/by-category", tags=['Productos'])
def get_products_by_category(request, category: str):
    products = ProductManager.get_products_by_category(category)
    if products:
        logger.info(f"Products found in category {category}: {products}")
        return {"ok": "yes", "data": products}
    else:
        logger.info(f"No products found in category {category}")
        return {"ok": "no", "error": "No products found in this category"}

@api.get("/products/by-title", tags=['Productos'])
def get_products_by_title(request, keyword: str):
    products = ProductManager.get_products_with_keyword_in_name(keyword)
    if products:
        logger.info(f"Products found with title {keyword}: {products}")
        return {"ok": "yes", "data": products}
    else:
        logger.info(f"No products found with title {keyword}")
        return {"ok": "no", "error": "No products found with this title"}

@api.get("/products/{product_id}", tags=['Productos'])
def get_product_by_id(request, product_id: str):
    product = ProductManager.get_product_by_id(product_id)
    if product:
        logger.info(f"Product found: {product}")
        return {"ok": "yes", "data": product}
    else:
        logger.info(f"Product not found: {product_id}")
        return {"ok": "no", "error": "Product not found"}


@api.post("/products", tags=['Productos'])
def add_product(request, product_in: ProductSchemaIn, image: UploadedFile = File(None)):
    product_data = product_in.dict()

    if image:
        image_path = save_image_and_get_path(image)
        product_data['image'] = image_path
    else:
        product_data['image'] = None

    ProductManager.add_product_to_collection(product_data)
    logger.info(f"Product added: {product_data}")
    return {"ok": "yes", "data": product_data}

@api.put("/products/{product_id}", tags=['Productos'])
def update_product(request, product_id: str, product_update: ProductSchemaIn):
    product = ProductManager.get_product_by_id(product_id)
    if not product:
        return {"ok": "no", "error": "Product not found"}

    try:
        updated_product = ProductManager.update_product(product_id, product_update.dict(exclude_unset=True))
        logger.info(f"Product updated: {updated_product}")
        return {"ok": "yes", "data": updated_product}
    except Exception as e:
        logger.error(f"Error updating product: {e}")
        return {"ok": "no", "error": str(e)}

@api.delete("/products/{product_id}", tags=['Productos'])
def delete_product(request, product_id: str):
	product = ProductManager.get_product_by_id(product_id)
	if not product:
		return {"ok": "no", "error": "Product not found"}

	try:
		ProductManager.delete_product(product_id)
		logger.info(f"Product deleted: {product}")
		return {"ok": "yes", "data": product}
	except Exception as e:
		logger.error(f"Error deleting product: {e}")
		return {"ok": "no", "error": str(e)}