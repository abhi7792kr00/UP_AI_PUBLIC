from core.database.session import SessionLocal
from app.dependencies.database import get_db


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()