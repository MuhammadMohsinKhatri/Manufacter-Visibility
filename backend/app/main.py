from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database.database import engine, Base, get_db
from app.routers import orders_router, inventory_router, production_router, supply_chain_router
from app.models import models

# Create tables
Base.metadata.create_all(bind=engine)

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
        # Try to execute a simple query
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}