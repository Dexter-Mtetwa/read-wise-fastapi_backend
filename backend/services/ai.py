import os
import json
from openai import OpenAI

client = None

def get_client():
    global client
    if client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            client = OpenAI(api_key=api_key)
    return client

# Load prompts from files
def load_chapter_prompt():
    """Load the chapter-level prompt from the markdown file."""
    prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "chapter_level_prompt.md")
    try:
        with open(prompt_path, 'r') as f:
            content = f.read()
            # Extract the prompt (remove markdown quote markers)
            prompt = content.strip().replace('> ', '').replace('>', '')
            return prompt
    except Exception as e:
        print(f"Error loading chapter prompt: {e}")
        return "You are an expert reading coach. Analyze the chapter and provide summary, key points, and questions in JSON format."

def load_book_prompt():
    """Load the book-level prompt from the markdown file."""
    prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "book_level_prompt.md")
    try:
        with open(prompt_path, 'r') as f:
            content = f.read()
            # Extract the prompt (remove markdown quote markers)
            prompt = content.strip().replace('> ', '').replace('>', '')
            return prompt
    except Exception as e:
        print(f"Error loading book prompt: {e}")
        return "You are an expert reading coach. Analyze the book and provide overview summary, key points, and questions in JSON format."

def process_chapter(chapter_text: str, chapter_title: str = "Chapter") -> dict:
    """
    Process a single chapter using the chapter-level prompt.
    Returns: {summary: str, key_points: list, questions: list}
    """
    client = get_client()
    if not client:
        return {
            "summary": "AI Client not configured.",
            "key_points": ["AI processing unavailable"],
            "questions": ["AI processing unavailable"]
        }
    
    try:
        prompt = load_chapter_prompt()
        user_message = f"{prompt}\n\nChapter Title: {chapter_title}\n\nChapter Text:\n{chapter_text}"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert reading coach and strategist. Always respond with valid JSON."},
                {"role": "user", "content": user_message}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # Ensure the expected keys exist
        return {
            "summary": result.get("summary", ""),
            "key_points": result.get("key_points", []),
            "questions": result.get("questions", [])
        }
    except Exception as e:
        print(f"Error processing chapter '{chapter_title}': {e}")
        return {
            "summary": f"Error processing chapter: {str(e)}",
            "key_points": ["Error generating key points"],
            "questions": ["Error generating questions"]
        }

def process_book_overview(full_text: str, book_title: str) -> dict:
    """
    Process the entire book to generate book-level overview.
    Returns: {overview_summary: str, overview_key_points: list, overview_questions: list}
    """
    client = get_client()
    if not client:
        return {
            "overview_summary": "AI Client not configured.",
            "overview_key_points": ["AI processing unavailable"],
            "overview_questions": ["AI processing unavailable"]
        }
    
    try:
        prompt = load_book_prompt()
        user_message = f"{prompt}\n\nBook Title: {book_title}\n\nBook Text:\n{full_text}"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert reading coach and strategist. Always respond with valid JSON."},
                {"role": "user", "content": user_message}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # Ensure the expected keys exist
        return {
            "overview_summary": result.get("overview_summary", ""),
            "overview_key_points": result.get("overview_key_points", []),
            "overview_questions": result.get("overview_questions", [])
        }
    except Exception as e:
        print(f"Error processing book overview for '{book_title}': {e}")
        return {
            "overview_summary": f"Error processing book overview: {str(e)}",
            "overview_key_points": ["Error generating key points"],
            "overview_questions": ["Error generating questions"]
        }

# Legacy functions for backward compatibility (deprecated)
def generate_summary(text: str) -> str:
    """
    DEPRECATED: Use process_chapter or process_book_overview instead.
    Generate a summary for the given text using OpenAI.
    """
    client = get_client()
    if not client:
        return "AI Client not configured."
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Summarize the following text:\n\n{text[:2000]}"} # Truncate for safety
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Error generating summary."

def generate_key_points(text: str) -> str:
    """
    DEPRECATED: Use process_chapter or process_book_overview instead.
    Extract key points from the text.
    """
    client = get_client()
    if not client:
        return "AI Client not configured."
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts key points from text."},
                {"role": "user", "content": f"Extract 3-5 key points from the following text:\n\n{text[:2000]}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating key points: {e}")
        return "Error generating key points."

def generate_questions(text: str) -> str:
    """
    DEPRECATED: Use process_chapter or process_book_overview instead.
    Generate discussion questions from the text.
    """
    client = get_client()
    if not client:
        return "AI Client not configured."
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates discussion questions."},
                {"role": "user", "content": f"Generate 3 thought-provoking discussion questions based on the following text:\n\n{text[:2000]}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating questions: {e}")
        return "Error generating questions."
