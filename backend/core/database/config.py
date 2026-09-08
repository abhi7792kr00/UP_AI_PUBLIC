from pathlib import Path

# Project Root Folder
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SQLite Database Location
DATABASE_URL = f"sqlite:///{BASE_DIR}/database/sqlite/up_ai.db"