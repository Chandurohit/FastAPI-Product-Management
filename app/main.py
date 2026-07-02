import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging import setup_logging
from app.database.session import engine, SessionLocal
from app.database.base import Base
# Import all database models to ensure they are registered on the Base metadata
from app.models.product_model import Product as DBProduct
from app.models.user_model import User as DBUser
from app.schemas.product_schema import Product as ProductSchema
from app.api.v1.products import router as products_router
from app.api.v1.auth import router as auth_router

logger = logging.getLogger(__name__)

# Configure logging structure
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks: Create database tables (both products and users)
    logger.info("Initializing database schema...")
    Base.metadata.create_all(bind=engine)
    
    # Startup tasks: Seed initial products if DB is empty
    logger.info("Checking database data...")
    db = SessionLocal()
    try:
        count = db.query(DBProduct).count()
        if count == 0:
            logger.info("Seeding default products...")
            initial_products = [
                ProductSchema(id=1, name="Laptop", description="A high-performance laptop", price=999.99, quantity=10),
                ProductSchema(id=2, name="Smartphone", description="A powerful smartphone", price=489.99, quantity=20),
                ProductSchema(id=3, name="Headphones", description="Noise-cancelling headphones", price=199.99, quantity=15),
                ProductSchema(id=4, name="Smartwatch", description="A stylish smartwatch", price=149.99, quantity=25),
            ]
            for product in initial_products:
                db.add(DBProduct(**product.model_dump()))
            db.commit()
            logger.info("Database seeding complete.")
        else:
            logger.info("Database already populated. Skipping seeding.")
    except Exception as e:
        logger.error(f"Error during database initialization/seeding: {e}")
        db.rollback()
    finally:
        db.close()
        
    yield
    # Shutdown tasks
    logger.info("Cleaning up backend resources...")

app = FastAPI(lifespan=lifespan)

# CORS middleware supporting credentials and dynamic origins (local + vercel/render deploys)
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?|https://.*\.vercel\.app|https://.*\.onrender\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(products_router, prefix="/api/v1")
app.include_router(products_router) # Legacy support

# Mount authentication routers
app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(auth_router, prefix="/auth") # Legacy support

@app.get("/")
def greet():
    """Default greeting endpoint."""
    return "HI my name is rohit"
