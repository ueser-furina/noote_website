from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 關聯到筆記
    notes = relationship("Note", back_populates="owner", cascade="all, delete-orphan")

    # 關聯到合集
    collections = relationship("Collection", back_populates="owner", cascade="all, delete-orphan")
