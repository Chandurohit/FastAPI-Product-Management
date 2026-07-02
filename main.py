"""
Compatibility layer for FastAPI startup commands and deployment platforms (e.g., Render, Vercel).
Exposes the main FastAPI application instance 'app' from the refactored modular app directory.
"""

from app.main import app