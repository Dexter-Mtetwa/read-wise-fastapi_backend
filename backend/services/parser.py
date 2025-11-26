import io
import re
from pypdf import PdfReader
from typing import List, Dict

def parse_file(file_content: bytes, filename: str) -> str:
    """
    Extract text from a PDF file.
    """
    if filename.lower().endswith(".pdf"):
        try:
            reader = PdfReader(io.BytesIO(file_content))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return ""
    # Placeholder for EPUB or other formats
    return ""

def parse_book_to_chapters(file_content: bytes, filename: str) -> List[Dict[str, any]]:
    """
    Parse a book file and extract chapters with titles.
    Returns: List of dicts with {title: str, text: str, index: int}
    """
    # First, extract the full text
    full_text = parse_file(file_content, filename)
    
    if not full_text:
        return []
    
    chapters = []
    
    # Try to detect chapter boundaries using common patterns
    # Patterns to match: "Chapter 1", "Chapter I", "CHAPTER ONE", etc.
    chapter_patterns = [
        r'(?i)^chapter\s+(\d+|[IVXLCDM]+|one|two|three|four|five|six|seven|eight|nine|ten)[:\s\-]',  # Chapter 1, Chapter I, Chapter One
        r'(?i)^(\d+|[IVXLCDM]+)\.\s+[A-Z]',  # 1. Title, I. Title
        r'(?i)^part\s+(\d+|[IVXLCDM]+|one|two|three)[:\s\-]',  # Part 1, Part I
    ]
    
    # Split by lines and look for chapter markers
    lines = full_text.split('\n')
    chapter_starts = []
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        for pattern in chapter_patterns:
            if re.match(pattern, line_stripped) and len(line_stripped) < 100:  # Chapter titles are usually short
                chapter_starts.append((i, line_stripped))
                break
    
    # If we found chapter markers, split the text
    if chapter_starts:
        for idx, (line_num, title) in enumerate(chapter_starts):
            # Determine the end of this chapter
            if idx < len(chapter_starts) - 1:
                next_line_num = chapter_starts[idx + 1][0]
            else:
                next_line_num = len(lines)
            
            # Extract chapter text
            chapter_lines = lines[line_num:next_line_num]
            chapter_text = '\n'.join(chapter_lines).strip()
            
            # Clean up the title
            chapter_title = title.strip()
            
            chapters.append({
                "index": idx,
                "title": chapter_title,
                "text": chapter_text
            })
    else:
        # Fallback: split by significant paragraph breaks (3+ newlines)
        # or create chunks of reasonable size
        chunks = re.split(r'\n{3,}', full_text)
        chunks = [c.strip() for c in chunks if c.strip() and len(c.strip()) > 200]
        
        # If we have reasonable chunks, use them as chapters
        if len(chunks) > 1:
            for idx, chunk in enumerate(chunks):
                # Try to extract a title from the first line
                first_line = chunk.split('\n')[0].strip()
                if len(first_line) < 100:
                    title = first_line
                else:
                    title = f"Section {idx + 1}"
                
                chapters.append({
                    "index": idx,
                    "title": title,
                    "text": chunk
                })
        else:
            # Last resort: treat the whole book as one chapter
            chapters.append({
                "index": 0,
                "title": "Full Text",
                "text": full_text
            })
    
    return chapters
