import io
from pypdf import PdfReader

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
