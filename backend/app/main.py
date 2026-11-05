import time
from contextlib import asynccontextmanager
from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from .database import Base,engine,get_db
from .models import Product
from .schemas import ProductCreate

@asynccontextmanager
async def lifespan(app):
    for _ in range(30):
        try:
            Base.metadata.create_all(bind=engine)
            break
        except OperationalError:
            time.sleep(2)
    yield

app=FastAPI(title="TerraSip MVP v2 Fixed", lifespan=lifespan)

@app.get("/health")
def health(): return {"status":"healthy"}

@app.post("/products")
def create_product(product:ProductCreate, db:Session=Depends(get_db)):
    p=Product(name=product.name, stock=product.stock)
    db.add(p); db.commit(); db.refresh(p)
    return {"id":p.id,"name":p.name,"stock":p.stock}

@app.get('/products')
def products(db:Session=Depends(get_db)):
    return db.query(Product).all()

@app.get('/inventory/check')
def inventory_check(db:Session=Depends(get_db)):
    low=db.query(Product).filter(Product.stock<20).all()
    return {"agent":"InventoryAgent","alerts":[{"id":x.id,"name":x.name,"stock":x.stock} for x in low]}
