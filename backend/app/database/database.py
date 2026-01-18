from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Database connection settings
# Default to SQLite (easy to use, no setup required)
# The database file will be created in the backend directory
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./manufacter_visibility.db")

# Create SQLAlchemy engine
# SQLite-specific settings:
# - check_same_thread=False: allows SQLite to work with FastAPI's async nature
# - echo=False: set to True for SQL query logging during development
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False  # Set to True for SQL query logging
)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()