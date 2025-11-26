# ReadWise Backend API

FastAPI backend for ReadWise - An AI-powered book reading and summarization platform.

## Features

- 📚 Upload PDF books
- 🤖 AI-powered chapter summarization (using GPT-4o-mini)
- 🔑 Key points extraction
- ❓ Reflective questions generation
- 📖 Book-level overview analysis
- 🔐 Supabase JWT authentication
- 🔒 Row Level Security (RLS) support

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (Supabase)
- **ORM**: SQLAlchemy
- **AI**: OpenAI GPT-4o-mini
- **Auth**: Supabase JWT
- **PDF Parsing**: PyPDF

## Local Development

### Prerequisites

- Python 3.8+
- PostgreSQL (or Supabase account)
- OpenAI API key

### Setup

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd backend
```

2. **Create virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file:

```env
DATABASE_URL=postgresql://user:password@host:5432/database
SUPABASE_JWT_SECRET=your-jwt-secret
OPENAI_API_KEY=your-openai-api-key
```

5. **Run the server**

```bash
uvicorn main:app --reload --port 8000
```

Server will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

## Authentication

See [AUTHENTICATION.md](./AUTHENTICATION.md) for authentication setup and usage.

## API Endpoints

### Public Endpoints

- `GET /health` - Health check

### Protected Endpoints (Require JWT)

- `POST /books` - Upload a book
- `GET /books` - List all books
- `GET /books/{book_id}` - Get book details
- `GET /books/{book_id}/chapters` - Get book chapters
- `GET /books/{book_id}/chapters/{chapter_index}` - Get chapter details
- `DELETE /books/{book_id}` - Delete a book

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `SUPABASE_JWT_SECRET` | Supabase JWT secret for token verification | Yes |
| `OPENAI_API_KEY` | OpenAI API key for AI processing | Yes |

## License

MIT
