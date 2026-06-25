from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session, engine, get_db
import database_models
from sqlalchemy.orm import Session


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "HI my name is rohit"
products = [
    Product(id=1, name="Laptop", description="A high-performance laptop", price=999.99, quantity=10),
    Product(id=2, name="Smartphone", description="A powerful smartphone", price=489.99, quantity=20),
    Product(id=3, name="Headphones", description="Noise-cancelling headphones",price=199.99, quantity=15),
    Product(id=4, name="Smartwatch", description="A stylish smartwatch", price=149.99, quantity=25),
]

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = session()

    count=db.query(database_models.Product).count()
    if count==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
        db.close()
init_db()

@app.get("/products")

def get_all_products(db: Session = Depends(get_db)):
    db_Products = db.query(database_models.Product).all()
    return db_Products

@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session=Depends(get_db)):
    db_products = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_products:
            return db_products
    return "product not found"

@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id: int, updated_product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = updated_product.name
        db_product.description = updated_product.description
        db_product.price = updated_product.price
        db_product.quantity = updated_product.quantity
        db.commit()
        return "product updated successfully"
    return "product not found"


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "product deleted successfully"
    return "product not found"