from decouple import config
from pydantic import BaseModel

class Settings(BaseModel):
    """Application settings"""
    DATABASE_URL: str = config('DATABASE_URL')
    VECTOR_DB_API_KEY: str = config('VECTOR_DB_API_KEY')
    VECTOR_DB_ENVIRONMENT: str = config('VECTOR_DB_ENVIRONMENT')
    OPENAI_API_KEY: str = config('OPENAI_API_KEY')
    PORT: int = config('PORT', default=8000, cast=int)

    class Config:
        env_file = ".env"

# Print debug info
settings = Settings()
print(f"OpenAI API Key configured: {'Yes' if settings.OPENAI_API_KEY else 'No'}")