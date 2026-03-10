from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

ALCHEMY_DATABASE_URL = 'postgresql://postgres:root@localhost:5432/fastapi'

engine = create_engine(ALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
         db.close()