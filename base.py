#base.py
from sqlalchemy.orm import DeclarativeBase,sessionmaker
from urllib.parse import quote_plus
from sqlalchemy import create_engine

# ==========================================
# DATABASE CONFIGURATION (SUPABASE POSTGRESQL)
# ==========================================
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Entity Base Class
class Base(DeclarativeBase):
    pass

# Database Credentials
DB_USER = os.getenv("DB_USER", "")
RAW_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_PASSWORD = quote_plus(RAW_PASSWORD)
DB_HOST = os.getenv("DB_HOST", "aws-0-ap-northeast-1.pooler.supabase.com")
DB_PORT = os.getenv("DB_PORT", "6543")
DB_NAME = os.getenv("DB_NAME", "postgres")

# DB_URL for SQLAlchemy with psycopg2
DB_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Create Engine
engine = create_engine(
    DB_URL,
    echo=False,
    pool_pre_ping=True
)

# Session Factory
Session = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

