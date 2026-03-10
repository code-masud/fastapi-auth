
from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, text

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))