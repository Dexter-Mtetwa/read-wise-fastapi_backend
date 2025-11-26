from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import uuid
import time
from dotenv import load_dotenv
from services import store, parser, ai

load_dotenv()

app = FastAPI(title="ReadWise API")

# Pydantic model for book response
class Book(BaseModel):
    id: str
    title: str
    status: str
    chapter_count: int = 0
    summary: Optional[str] = None

@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Background task to process book and generate summary
def process_book_background(book_id: str, text: str):
    """
    Background task to process book and generate summary.
    """

    print(f"Starting background processing for book {book_id}")
    summary = ai.generate_summary(text)
    if book_id in store.books:
        store.books[book_id]["summary"] = summary
        store.books[book_id]["status"] = "completed"
    print(f"Finished background processing for book {book_id}")

# API endpoint to upload a book
@app.post("/books", response_model=Book)
async def upload_book(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Upload a PDF/EPUB file, parse it, and store it in memory.
    Triggers background AI summarization.
    """

    content = await file.read()
    text = parser.parse_file(content, file.filename)
    
    if not text:
        raise HTTPException(status_code=400, detail="Could not parse file or empty content")
    
    book_id = str(uuid.uuid4())
    # Simple chapter splitting by double newline for MWV
    chapters = [c.strip() for c in text.split("\n\n") if c.strip()]
    
    # Store book in memory
    store.books[book_id] = {
        "id": book_id,
        "title": file.filename,
        "status": "processing", # Changed to processing
        "content": text,
        "chapters": chapters,
        "created_at": time.time(),
        "summary": None
    }
    
    # Trigger background task
    background_tasks.add_task(process_book_background, book_id, text)
    
    # Return book info 
    return {
        "id": book_id,
        "title": file.filename,
        "status": "processing",
        "chapter_count": len(chapters)
    }

# API endpoint to get a book
@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: str):
    if book_id not in store.books:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book = store.books[book_id]
    return {
        "id": book["id"],
        "title": book["title"],
        "status": book["status"],
        "chapter_count": len(book["chapters"]),
        "summary": book.get("summary")
    }

@app.get("/books/{book_id}/chapters")
async def get_book_chapters(book_id: str):
    if book_id not in store.books:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return {"chapters": store.books[book_id]["chapters"]}

