from routes.royalty_apis import router as royalty_router
from database.database import engine, SessionLocal
from contextlib import asynccontextmanager
from models.royalty_models import Base
from fastapi import FastAPI
from seed import seed_data
from utils.logger import get_logger
from fastapi.middleware.cors import CORSMiddleware

logger = get_logger("MainApp")

# This function is used to seed database with provided dummy data
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    logger.info("Application startup initiated")
    Base.metadata.create_all(bind=engine)
    # Seed database
    db = SessionLocal()
    try:
        seed_data(db)
        logger.info("Database seeded successfully")
    except Exception as e:
        logger.error(f"Seeding failed: {e}")
    finally:
        db.close()

    logger.info("Application started")
    yield 
    logger.info("Application shutting down")
    
# Create FastAPI app
app = FastAPI(
    title="BookLeaf Royalty API",
    description="REST API for Author Royalty System",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(royalty_router, tags=["Royalties"])   #prefix="/api/v1"

# Health check route
@app.get("/")
def health_check():
    return {
        "status": "OK",
        "message": "BookLeaf Royalty API is running"
    }