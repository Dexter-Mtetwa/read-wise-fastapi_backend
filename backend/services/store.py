from sqlalchemy.orm import Session
from services.models import Book, Chapter
from services.database import SessionLocal
from typing import List, Optional, Dict, Any
import json

"""

"""

# Helper to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Book Operations ---

def create_book(book_data: Dict[str, Any]) -> Book:
    db = SessionLocal()
    try:
        # Convert list fields to proper JSON if needed, though SQLAlchemy JSON type handles python lists/dicts
        # Ensure we don't pass fields that aren't in the model if the dict has extras
        
        new_book = Book(
            id=book_data.get("id"),
            title=book_data.get("title"),
            status=book_data.get("status", "processing"),
            owner_id=book_data.get("owner_id"),
            chapter_count=book_data.get("chapter_count", 0),
            overview_summary=book_data.get("overview_summary"),
            overview_key_points=book_data.get("overview_key_points"),
            overview_questions=book_data.get("overview_questions")
        )
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
    finally:
        db.close()

def get_book(book_id: str) -> Optional[Dict[str, Any]]:
    db = SessionLocal()
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            return None
        return _book_to_dict(book)
    finally:
        db.close()

def get_all_books() -> Dict[str, Any]:
    # Returning a dict to maintain compatibility with existing code structure where possible,
    # or we can return a list. The original code used store.books.values().
    # Let's return a dict keyed by ID to match the previous store.books interface if we want to minimize changes,
    # BUT the previous store.books was the dict itself.
    # The calling code does `store.books.values()`. 
    # So we should probably change the calling code to call a function.
    # For now, let's provide a function that returns the list of dicts.
    db = SessionLocal()
    try:
        books = db.query(Book).all()
        return {book.id: _book_to_dict(book) for book in books}
    finally:
        db.close()

def update_book(book_id: str, data: Dict[str, Any]):
    db = SessionLocal()
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if book:
            for key, value in data.items():
                if hasattr(book, key):
                    setattr(book, key, value)
            db.commit()
            db.refresh(book)
            return _book_to_dict(book)
        return None
    finally:
        db.close()

def delete_book(book_id: str):
    db = SessionLocal()
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if book:
            db.delete(book)
            db.commit()
            return True
        return False
    finally:
        db.close()

# --- Chapter Operations ---

def create_chapter(chapter_data: Dict[str, Any]):
    db = SessionLocal()
    try:
        new_chapter = Chapter(
            id=chapter_data.get("id"),
            book_id=chapter_data.get("book_id"),
            owner_id=chapter_data.get("owner_id"),
            chapter_index=chapter_data.get("chapter_index"),
            title=chapter_data.get("title"),
            text=chapter_data.get("text"),
            summary=chapter_data.get("summary"),
            key_points=chapter_data.get("key_points"),
            questions=chapter_data.get("questions")
        )
        db.add(new_chapter)
        db.commit()
        db.refresh(new_chapter)
        return _chapter_to_dict(new_chapter)
    finally:
        db.close()

def get_chapter(chapter_id: str) -> Optional[Dict[str, Any]]:
    db = SessionLocal()
    try:
        chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
        if not chapter:
            return None
        return _chapter_to_dict(chapter)
    finally:
        db.close()

def get_book_chapters(book_id: str) -> List[Dict[str, Any]]:
    db = SessionLocal()
    try:
        chapters = db.query(Chapter).filter(Chapter.book_id == book_id).order_by(Chapter.chapter_index).all()
        return [_chapter_to_dict(ch) for ch in chapters]
    finally:
        db.close()

def update_chapter(chapter_id: str, data: Dict[str, Any]):
    db = SessionLocal()
    try:
        chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
        if chapter:
            for key, value in data.items():
                if hasattr(chapter, key):
                    setattr(chapter, key, value)
            db.commit()
            db.refresh(chapter)
            return _chapter_to_dict(chapter)
        return None
    finally:
        db.close()

# --- Helpers ---

def _book_to_dict(book: Book) -> Dict[str, Any]:
    return {
        "id": book.id,
        "title": book.title,
        "status": book.status,
        "owner_id": str(book.owner_id) if book.owner_id else None,
        "chapter_count": book.chapter_count,
        "overview_summary": book.overview_summary,
        "overview_key_points": book.overview_key_points,
        "overview_questions": book.overview_questions,
        "created_at": book.created_at.isoformat() if book.created_at else None
    }

def _chapter_to_dict(chapter: Chapter) -> Dict[str, Any]:
    return {
        "id": chapter.id,
        "book_id": chapter.book_id,
        "owner_id": str(chapter.owner_id) if chapter.owner_id else None,
        "chapter_index": chapter.chapter_index,
        "title": chapter.title,
        "text": chapter.text,
        "summary": chapter.summary,
        "key_points": chapter.key_points,
        "questions": chapter.questions
    }

# Compatibility layers for direct dict access if needed, 
# but we should refactor main.py to use functions instead of accessing these directly.
# These are now effectively "virtual" stores accessed via functions.
books = {} 
chapters = {}
