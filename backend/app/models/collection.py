from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, default="")
    cover_image = Column(String, nullable=True)  # 封面圖片 URL
    is_public = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 關聯到用戶
    owner = relationship("User", back_populates="collections")

    # 關聯到 CollectionNote（合集中的筆記）
    collection_notes = relationship("CollectionNote", back_populates="collection", cascade="all, delete-orphan")


class CollectionNote(Base):
    __tablename__ = "collection_notes"

    id = Column(Integer, primary_key=True, index=True)
    collection_id = Column(Integer, ForeignKey("collections.id"), nullable=False)
    note_id = Column(Integer, ForeignKey("notes.id"), nullable=False)
    position = Column(Integer, default=0)  # 排序位置
    added_at = Column(DateTime, default=datetime.utcnow)

    # 關聯
    collection = relationship("Collection", back_populates="collection_notes")
    note = relationship("Note")
