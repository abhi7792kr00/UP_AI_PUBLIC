from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.database.config import DATABASE_URL


# SQLite and PostgreSQL need slightly different engine settings.
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False,
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=1800,
        echo=False,
    )


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
