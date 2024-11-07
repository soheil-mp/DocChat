from fastapi import Request
from fastapi.responses import JSONResponse

async def openai_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=503,
        content={"detail": "AI service temporarily unavailable"}
    )

async def vector_db_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=503,
        content={"detail": "Vector database service unavailable"}
    ) 