from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI(title="TerraSip MVP")
PRODUCTS=[]

class Product(BaseModel):
    name:str
    stock:int

@app.get("/health")
def health():
    return {"status":"healthy"}

@app.get('/products')
def get_products():
    return PRODUCTS

@app.post('/products')
def create_product(product:Product):
    PRODUCTS.append(product.model_dump())
    return product

@app.get('/inventory/check')
def inventory_check():
    alerts=[p for p in PRODUCTS if p['stock']<20]
    return {"alerts":alerts,"agent":"InventoryAgent"}
