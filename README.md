# ReadWise Backend

ReadWise is an AI-powered reading assistant that helps you retain more from your books. This is the backend service built with FastAPI.

## Features

- **PDF Upload & Parsing**: Upload PDF files and automatically extract text.
- **AI Summarization**: Generates concise summaries of chapters using OpenAI.
- **Background Processing**: Handles heavy AI tasks asynchronously to keep the UI responsive.
- **In-Memory Store**: Lightweight storage for the MVP (Minimum Working Version).

## Tech Stack

- **Framework**: FastAPI (Python)
- **AI**: OpenAI API
- **PDF Processing**: pypdf
- **Task Queue**: FastAPI BackgroundTasks

## Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Dexter-Mtetwa/read-wise-fastapi_backend.git
    cd read-wise-fastapi_backend
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

4.  **Configure Environment**:
    Create a `.env` file in the `backend` directory:
    ```bash
    OPENAI_API_KEY=your_openai_api_key_here
    ```

## Running the Server

Navigate to the `backend` directory and run:

```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`.

## API Usage

### Upload a Book
```bash
curl -X POST -F "file=@/path/to/book.pdf" http://localhost:8000/books
```

### Get Book Status & Summary
```bash
curl http://localhost:8000/books/{book_id}
```

### Get Chapters
```bash
curl http://localhost:8000/books/{book_id}/chapters
```
