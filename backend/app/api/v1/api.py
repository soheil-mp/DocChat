from fastapi import APIRouter
from .endpoints import documents, chat

api_router = APIRouter()

# Include document routes
api_router.include_router(
    documents.router,
    prefix="/documents",
    tags=["documents"]
)

# Include chat routes
api_router.include_router(
    chat.router,
    prefix="/chat",
    tags=["chat"]
) 