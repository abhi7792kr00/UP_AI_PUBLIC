from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.database.config import DATABASE_URL

# SQLite Engine
engine = create_engine(
    DATABASE_URL,
    echo=True
)

# Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)