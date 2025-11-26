from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from services.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Book(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    status = Column(String, default="processing")  # processing, completed, error
    chapter_count = Column(Integer, default=0)
    
    # AI Analysis
    overview_summary = Column(Text, nullable=True)
    overview_key_points = Column(JSON, nullable=True)
    overview_questions = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    chapters = relationship("Chapter", back_populates="book", cascade="all, delete-orphan")

class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(String, primary_key=True) # format: {book_id}_chapter_{index}
    book_id = Column(String, ForeignKey("books.id"), nullable=False)
    chapter_index = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    
    # AI Analysis
    summary = Column(Text, nullable=True)
    key_points = Column(JSON, nullable=True)
    questions = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    book = relationship("Book", back_populates="chapters")
