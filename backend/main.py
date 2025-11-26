from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
import time
from dotenv import load_dotenv
from services import store, parser, ai
from services.database import init_db
from services.auth import get_current_user_id

load_dotenv()

app = FastAPI(title="ReadWise API")

# CORS Configuration - Allow frontend to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

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
def process_book_background(book_id: str, chapters_data: list, book_title: str, owner_id: Optional[str] = None):
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
            
            # Store chapter in database
            store.create_chapter({
                "id": chapter_id,
                "book_id": book_id,
                "owner_id": owner_id,
                "chapter_index": chapter_data['index'],
                "title": chapter_title,
                "text": chapter_text,
                "summary": chapter_result.get("summary"),
                "key_points": chapter_result.get("key_points", []),
                "questions": chapter_result.get("questions", [])
            })
        
        # Step 3: Generate book-level overview
        print(f"Generating book-level overview for {book_title}")
        book_result = ai.process_book_overview(full_text, book_title)
        
        # Step 4: Update book with overview and mark as completed
        store.update_book(book_id, {
            "overview_summary": book_result.get("overview_summary"),
            "overview_key_points": book_result.get("overview_key_points", []),
            "overview_questions": book_result.get("overview_questions", []),
            "status": "completed"
        })
        
        print(f"Finished background processing for book {book_id}")
    except Exception as e:
        print(f"Error in background processing for book {book_id}: {e}")
        store.update_book(book_id, {"status": "error"})

# API endpoint to upload a book
@app.post("/books", response_model=Book)
async def upload_book(
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...),
    current_user_id: str = Depends(get_current_user_id)
):
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
    
    # Store book in database with initial state
    new_book = store.create_book({
        "id": book_id,
        "title": file.filename,
        "status": "processing",
        "owner_id": current_user_id,
        "chapter_count": len(chapters_data),
        "overview_summary": None,
        "overview_key_points": None,
        "overview_questions": None
    })
    
    # Trigger background task for comprehensive processing
    background_tasks.add_task(process_book_background, book_id, chapters_data, file.filename, current_user_id)
    
    # Return book info (convert SQLAlchemy model/dict to response model)
    # store.create_book returns the Book object, we can return it directly or convert to dict
    return {
        "id": new_book.id,
        "title": new_book.title,
        "status": new_book.status,
        "chapter_count": new_book.chapter_count,
        "overview_summary": new_book.overview_summary,
        "overview_key_points": new_book.overview_key_points,
        "overview_questions": new_book.overview_questions
    }

# API endpoint to list all books
@app.get("/books", response_model=List[Book])
async def list_books():
    """
    List all uploaded books with their overview data.
    """
    books_dict = store.get_all_books()
    # books_dict is {id: dict}
    return list(books_dict.values())

# API endpoint to delete a book
@app.delete("/books/{book_id}")
async def delete_book(book_id: str):
    """
    Delete a book and all its chapters.
    """
    success = store.delete_book(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return {"status": "deleted"}

# API endpoint to get a specific book
@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: str):
    """
    Get detailed information about a specific book including overview data.
    """
    book = store.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book

# API endpoint to get all chapters of a book
@app.get("/books/{book_id}/chapters", response_model=List[Chapter])
async def get_book_chapters(book_id: str):
    """
    Get all chapters for a book with their summaries, key points, and questions.
    Does not include the full chapter text.
    """
    # Check if book exists first
    if not store.get_book(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    
    return store.get_book_chapters(book_id)

# API endpoint to get a specific chapter with full text
@app.get("/books/{book_id}/chapters/{chapter_index}", response_model=ChapterDetail)
async def get_chapter_detail(book_id: str, chapter_index: int):
    """
    Get full details for a specific chapter including the chapter text.
    """
    if not store.get_book(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Find the chapter
    chapter_id = f"{book_id}_chapter_{chapter_index}"
    chapter = store.get_chapter(chapter_id)
    
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    return chapter
