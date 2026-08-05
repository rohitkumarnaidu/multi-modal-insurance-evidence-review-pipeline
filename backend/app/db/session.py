import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database URL should be loaded securely via secret manager or env
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:password@localhost:5432/claimsdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
