# ReadWise Backend MWV Walkthrough

I have successfully built the Minimum Working Version (MWV) of the ReadWise backend.

## Features Implemented
- **File Upload**: Upload PDF files via `/books`.
- **Parsing**: Automatically extracts text from PDFs.
- **AI Integration**: Generates summaries using OpenAI (requires API key).
- **Background Processing**: Handles AI tasks asynchronously.
- **In-Memory Store**: Stores book data temporarily.

## How to Run

1.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```

2.  **Activate the virtual environment**:
    ```bash
    source venv/bin/activate
    ```

3.  **Set your OpenAI API Key**:
    ```bash
    export OPENAI_API_KEY="your-api-key-here"
    ```

4.  **Run the server**:
    ```bash
    uvicorn main:app --reload
    ```

## Testing

### Upload a Book
```bash
curl -X POST -F "file=@test.pdf" http://localhost:8000/books
```

### Get Book Details
```bash
curl http://localhost:8000/books/{book_id}
```

### Get Chapters
```bash
curl http://localhost:8000/books/{book_id}/chapters
```

## Deployment (Vercel)

The project is configured for Vercel deployment.

1.  **Install Vercel CLI**:
    ```bash
    npm i -g vercel
    ```

2.  **Deploy**:
    ```bash
    vercel
    ```

3.  **Environment Variables**:
    Remember to add `OPENAI_API_KEY` in your Vercel Project Settings.
