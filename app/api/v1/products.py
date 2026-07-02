from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.product_schema import Product as ProductSchema
from app.services.product_service import ProductService
from app.utils.constants import PRODUCT_NOT_FOUND, PRODUCT_UPDATED_SUCCESS, PRODUCT_DELETED_SUCCESS

# Apply get_current_user dependency at the router level to protect all product endpoints
router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    """Retrieve all products."""
    return ProductService.get_all_products(db)

@router.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    """Retrieve a product by its ID."""
    product = ProductService.get_product_by_id(db, id)
    if product:
        return product
    return PRODUCT_NOT_FOUND

@router.post("/products")
def add_product(product: ProductSchema, db: Session = Depends(get_db)):
    """Add a new product."""
    ProductService.create_product(db, product)
    return product

@router.put("/products/{id}")
def update_product(id: int, updated_product: ProductSchema, db: Session = Depends(get_db)):
    """Update an existing product."""
    result = ProductService.update_product(db, id, updated_product)
    if result:
        return PRODUCT_UPDATED_SUCCESS
    return PRODUCT_NOT_FOUND

@router.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    """Delete a product by ID."""
    result = ProductService.delete_product(db, id)
    if result:
        return PRODUCT_DELETED_SUCCESS
    return PRODUCT_NOT_FOUND
