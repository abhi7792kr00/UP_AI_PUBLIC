from core.database.session import engine
from core.database.base import Base

# सभी Models Import करो
import database.models

# Database की सभी Tables बनाओ
Base.metadata.create_all(bind=engine)

print("✅ Database created successfully!")