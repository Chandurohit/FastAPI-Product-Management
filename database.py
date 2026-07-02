"""
Compatibility layer for database imports.
Imports and re-exports database configuration and dependency functions from the refactored package.
"""

from app.database.session import SessionLocal, engine
from app.dependencies import get_db