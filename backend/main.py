from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import uuid
import time
from dotenv import load_dotenv
from services import store, parser, ai

load_dotenv()

app = FastAPI(title="ReadWise API")

# Pydantic models
class Book(BaseModel):
    id: str
    title: str
    status: str
    chapter_count: int = 0
    overview_summary: Optional[str] = None
    overview_key_points: Optional[List[str]] = None
    overview_questions: Optional[List[str]] = None

class Chapter(BaseModel):
    id: str
    book_id: str
    chapter_index: int
    title: str
    summary: Optional[str] = None
    key_points: Optional[List[str]] = None
    questions: Optional[List[str]] = None

class ChapterDetail(BaseModel):
    id: str
    book_id: str
    chapter_index: int
    title: str
    text: str
    summary: Optional[str] = None
    key_points: Optional[List[str]] = None
    questions: Optional[List[str]] = None

@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Enhanced background task to process book with chapter-level and book-level analysis
def process_book_background(book_id: str, chapters_data: list, book_title: str):
    """
    Background task to process all chapters and generate book-level overview.
    Steps:
    1. Process each chapter with AI
    2. Store chapter results
    3. Generate book-level overview
    4. Mark book as completed
    """
    print(f"Starting background processing for book {book_id} with {len(chapters_data)} chapters")
    
    try:
        # Step 1 & 2: Process each chapter
        full_text = ""
        for chapter_data in chapters_data:
            chapter_id = f"{book_id}_chapter_{chapter_data['index']}"
            chapter_text = chapter_data['text']
            chapter_title = chapter_data['title']
            full_text += chapter_text + "\n\n"
            
            print(f"Processing chapter {chapter_data['index']}: {chapter_title}")
            
            # Process chapter with AI
            chapter_result = ai.process_chapter(chapter_text, chapter_title)
            
            # Store chapter in memory
            store.chapters[chapter_id] = {
                "id": chapter_id,
                "book_id": book_id,
                "chapter_index": chapter_data['index'],
                "title": chapter_title,
                "text": chapter_text,
                "summary": chapter_result.get("summary"),
                "key_points": chapter_result.get("key_points", []),
                "questions": chapter_result.get("questions", [])
            }
        
        # Step 3: Generate book-level overview
        print(f"Generating book-level overview for {book_title}")
        book_result = ai.process_book_overview(full_text, book_title)
        
        # Step 4: Update book with overview and mark as completed
        if book_id in store.books:
            store.books[book_id]["overview_summary"] = book_result.get("overview_summary")
            store.books[book_id]["overview_key_points"] = book_result.get("overview_key_points", [])
            store.books[book_id]["overview_questions"] = book_result.get("overview_questions", [])
            store.books[book_id]["status"] = "completed"
        
        print(f"Finished background processing for book {book_id}")
    except Exception as e:
        print(f"Error in background processing for book {book_id}: {e}")
        if book_id in store.books:
            store.books[book_id]["status"] = "error"

# API endpoint to upload a book
@app.post("/books", response_model=Book)
async def upload_book(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Upload a PDF/EPUB file, parse it into chapters, and trigger AI processing.
    Returns immediately with 'processing' status.
    """
    content = await file.read()
    
    # Parse book into chapters
    chapters_data = parser.parse_book_to_chapters(content, file.filename)
    
    if not chapters_data:
        raise HTTPException(status_code=400, detail="Could not parse file or empty content")
    
    book_id = str(uuid.uuid4())
    
    # Store book in memory with initial state
    store.books[book_id] = {
        "id": book_id,
        "title": file.filename,
        "status": "processing",
        "created_at": time.time(),
        "chapter_count": len(chapters_data),
        "overview_summary": None,
        "overview_key_points": None,
        "overview_questions": None
    }
    
    # Trigger background task for comprehensive processing
    background_tasks.add_task(process_book_background, book_id, chapters_data, file.filename)
    
    # Return book info
    return {
        "id": book_id,
        "title": file.filename,
        "status": "processing",
        "chapter_count": len(chapters_data)
    }

# API endpoint to list all books
@app.get("/books", response_model=List[Book])
async def list_books():
    """
    List all uploaded books with their overview data.
    """
    return [
        {
            "id": b["id"],
            "title": b["title"],
            "status": b["status"],
            "chapter_count": b.get("chapter_count", 0),
            "overview_summary": b.get("overview_summary"),
            "overview_key_points": b.get("overview_key_points"),
            "overview_questions": b.get("overview_questions")
        }
        for b in store.books.values()
    ]

# API endpoint to delete a book
@app.delete("/books/{book_id}")
async def delete_book(book_id: str):
    """
    Delete a book and all its chapters.
    """
    if book_id not in store.books:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Delete the book
    del store.books[book_id]
    
    # Delete all associated chapters
    chapter_ids_to_delete = [
        ch_id for ch_id, ch in store.chapters.items()
        if ch.get("book_id") == book_id
    ]
    for ch_id in chapter_ids_to_delete:
        del store.chapters[ch_id]
    
    return {"status": "deleted"}

# API endpoint to get a specific book
@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: str):
    """
    Get detailed information about a specific book including overview data.
    """
    if book_id not in store.books:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book = store.books[book_id]
    return {
        "id": book["id"],
        "title": book["title"],
        "status": book["status"],
        "chapter_count": book.get("chapter_count", 0),
        "overview_summary": book.get("overview_summary"),
        "overview_key_points": book.get("overview_key_points"),
        "overview_questions": book.get("overview_questions")
    }

# API endpoint to get all chapters of a book
@app.get("/books/{book_id}/chapters", response_model=List[Chapter])
async def get_book_chapters(book_id: str):
    """
    Get all chapters for a book with their summaries, key points, and questions.
    Does not include the full chapter text.
    """
    if book_id not in store.books:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Get all chapters for this book
    book_chapters = [
        {
            "id": ch["id"],
            "book_id": ch["book_id"],
            "chapter_index": ch["chapter_index"],
            "title": ch["title"],
            "summary": ch.get("summary"),
            "key_points": ch.get("key_points"),
            "questions": ch.get("questions")
        }
        for ch in store.chapters.values()
        if ch.get("book_id") == book_id
    ]
    
    # Sort by chapter index
    book_chapters.sort(key=lambda x: x["chapter_index"])
    
    return book_chapters

# API endpoint to get a specific chapter with full text
@app.get("/books/{book_id}/chapters/{chapter_index}", response_model=ChapterDetail)
async def get_chapter_detail(book_id: str, chapter_index: int):
    """
    Get full details for a specific chapter including the chapter text.
    """
    if book_id not in store.books:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Find the chapter
    chapter_id = f"{book_id}_chapter_{chapter_index}"
    
    if chapter_id not in store.chapters:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    chapter = store.chapters[chapter_id]
    return {
        "id": chapter["id"],
        "book_id": chapter["book_id"],
        "chapter_index": chapter["chapter_index"],
        "title": chapter["title"],
        "text": chapter["text"],
        "summary": chapter.get("summary"),
        "key_points": chapter.get("key_points"),
        "questions": chapter.get("questions")
    }
