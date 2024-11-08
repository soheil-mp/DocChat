from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.api.v1.endpoints import chat
from app.db.mongodb import db  # Import the MongoDB instance
from app.core.config import settings  # Add this import

app = FastAPI(
    title="DocuChat API",
    description="API for DocuChat - Knowledge Base Chat with RAG",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_db_client():
    """Initialize database connection on startup"""
    await db.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection on shutdown"""
    await db.close()

@app.get("/")
async def root():
    """
    Root endpoint that redirects to API documentation
    """
    return RedirectResponse(url="/docs")

# Update CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the chat router
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])