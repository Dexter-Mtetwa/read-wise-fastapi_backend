from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment variable
# Default to sqlite for development if not set, but we aim for Postgres
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    # Fallback or warning - for now let's assume the user will provide it
    # But to avoid crashing immediately if they haven't set it yet:
    print("WARNING: DATABASE_URL not set in .env")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./readwise.db"

# Handle special case for Supabase/Postgres where URL might start with postgres://
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Remove pgbouncer=true if present, as it causes issues with psycopg2
if "pgbouncer=true" in SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("?pgbouncer=true", "").replace("&pgbouncer=true", "")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    # Import models here to avoid circular imports
    from services import models
    Base.metadata.create_all(bind=engine)
