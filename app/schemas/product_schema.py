from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Laptop",
                "description": "A high-performance laptop",
                "price": 999.99,
                "quantity": 10
            }
        }
