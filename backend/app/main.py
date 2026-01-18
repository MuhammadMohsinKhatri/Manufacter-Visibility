from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database.database import engine, Base, get_db
from app.routers import orders_router, inventory_router, production_router, supply_chain_router
from app.routers import shipment_tracking
from app.models import models
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Manufacturing Visibility API",
    description="API for manufacturing visibility across order management, inventory, production, and supply chain",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(orders_router)
app.include_router(inventory_router)
app.include_router(production_router)
app.include_router(supply_chain_router)
app.include_router(shipment_tracking.router)

@app.on_event("startup")
async def startup_event():
    """Create database tables on startup (with error handling)"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified successfully")
    except Exception as e:
        logger.warning(f"Could not connect to database on startup: {e}")
        logger.warning("The application will start, but database operations may fail until the database is available.")

@app.get("/")
def read_root():
    return {
        "message": "Manufacturing Visibility API",
        "documentation": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint to verify database connection"""
    try:
        # Try to execute a simple query (works with both SQLite and MySQL)
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}