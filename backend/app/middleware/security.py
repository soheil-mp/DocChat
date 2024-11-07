from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from app.config import Settings

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(API_KEY_HEADER)):
    if api_key != Settings().API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key 