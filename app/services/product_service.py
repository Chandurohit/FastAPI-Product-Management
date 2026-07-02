from sqlalchemy.orm import Session
from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import Product as ProductSchema

class ProductService:
    @staticmethod
    def get_all_products(db: Session):
        """Service layer method to fetch all products."""
        return ProductRepository.get_all(db)

    @staticmethod
    def get_product_by_id(db: Session, product_id: int):
        """Service layer method to retrieve a product by ID."""
        return ProductRepository.get_by_id(db, product_id)

    @staticmethod
    def create_product(db: Session, product: ProductSchema):
        """Service layer method to create a new product."""
        return ProductRepository.create(db, product)

    @staticmethod
    def update_product(db: Session, product_id: int, updated_product: ProductSchema):
        """Service layer method to update an existing product."""
        return ProductRepository.update(db, product_id, updated_product)

    @staticmethod
    def delete_product(db: Session, product_id: int):
        """Service layer method to delete a product."""
        return ProductRepository.delete(db, product_id)
