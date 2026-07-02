"""
Compatibility layer for database models.
Imports and re-exports the SQLAlchemy Declarative Base and Product model.
"""

from app.database.base import Base
from app.models.product_model import Product