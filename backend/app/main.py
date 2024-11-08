from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.api.v1.endpoints import chat, documents
from app.db.mongodb import db
from app.core.config import settings

app = FastAPI(
    title="DocuChat API",
    description="API for DocuChat - Knowledge Base Chat with RAG",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_db_client():
    """Initialize database connection on startup"""
    await db.connect_to_database()

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection on shutdown"""
    await db.close_database_connection()

@app.get("/")
async def root():
    """
    Root endpoint that redirects to API documentation
    """
    return RedirectResponse(url="/docs")

# Update CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

# Include routers with proper prefixes
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])