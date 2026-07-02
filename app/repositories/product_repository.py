from sqlalchemy.orm import Session
from app.models.product_model import Product as DBProduct
from app.schemas.product_schema import Product as ProductSchema

class ProductRepository:
    @staticmethod
    def get_all(db: Session):
        """Retrieve all products from the database."""
        return db.query(DBProduct).all()

    @staticmethod
    def get_by_id(db: Session, product_id: int):
        """Retrieve a specific product by its ID."""
        return db.query(DBProduct).filter(DBProduct.id == product_id).first()

    @staticmethod
    def create(db: Session, product: ProductSchema):
        """Insert a new product record."""
        db_product = DBProduct(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def update(db: Session, product_id: int, updated_product: ProductSchema):
        """Update an existing product record if found."""
        db_product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
        if db_product:
            db_product.name = updated_product.name
            db_product.description = updated_product.description
            db_product.price = updated_product.price
            db_product.quantity = updated_product.quantity
            db.commit()
            db.refresh(db_product)
            return db_product
        return None

    @staticmethod
    def delete(db: Session, product_id: int):
        """Delete an existing product record if found."""
        db_product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
        if db_product:
            db.delete(db_product)
            db.commit()
            return db_product
        return None
