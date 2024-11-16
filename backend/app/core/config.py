from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List
import os
import json

class Settings(BaseSettings):
    # Base directories
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    DOCUMENTS_DIR: Path = BASE_DIR / "documents"
    
    # Server settings
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    
    # MongoDB settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "DocChat"
    
    # JWT settings
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API Keys and Environment
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_ENV: str
    PINECONE_INDEX_NAME: str = "DocChat"
    ANTHROPIC_API_KEY: str | None = None
    COHERE_API_KEY: str | None = None
    
    # File Storage
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB in bytes
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = str(Path(__file__).parent.parent.parent / '.env')
        env_file_encoding = 'utf-8'

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == 'BACKEND_CORS_ORIGINS':
                return json.loads(raw_val)
            return raw_val

settings = Settings()