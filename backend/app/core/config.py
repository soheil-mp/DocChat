import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Base directories
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    DOCUMENTS_DIR: Path = BASE_DIR / "documents"
    
    # Server settings
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    
    # MongoDB settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "docuchat"
    
    # JWT settings
    JWT_SECRET_KEY: str = "your_super_secret_key_here"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI settings
    OPENAI_API_KEY: str
    
    # Pinecone settings
    PINECONE_API_KEY: str
    PINECONE_ENV: str = "us-east-1"
    PINECONE_INDEX_NAME: str = "docuchat"
    
    # Other LLM Provider settings (optional)
    ANTHROPIC_API_KEY: Optional[str] = None
    COHERE_API_KEY: Optional[str] = None
    
    # File Upload settings
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB in bytes
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = str(Path(__file__).parent.parent.parent / '.env')  # Absolute path to .env
        case_sensitive = True
        env_file_encoding = 'utf-8'

# Initialize settings with explicit env file path
env_path = Path(__file__).parent.parent.parent / '.env'
print(f"Looking for .env file at: {env_path.absolute()}")
settings = Settings(_env_file=str(env_path))

# Create necessary directories
os.makedirs(settings.DOCUMENTS_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True) 