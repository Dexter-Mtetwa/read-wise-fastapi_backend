from typing import Dict, Any

# In-memory storage
# Books structure: {book_id: {id, title, status, content, overview_summary, overview_key_points, overview_questions, created_at}}
books: Dict[str, Any] = {}

# Chapters structure: {chapter_id: {id, book_id, chapter_index, title, text, summary, key_points, questions}}
chapters: Dict[str, Any] = {}
