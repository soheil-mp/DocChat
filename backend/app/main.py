from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .config import Settings
from .services.document_service import DocumentService
from .services.chat_service import ChatService
from .routes.chat import router as chat_router
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="DocuChat API")
settings = Settings()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
document_service = DocumentService()
chat_service = ChatService()

app.include_router(chat_router)

class ModelConfig(BaseModel):
    model: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    top_p: float | None = None
    frequency_penalty: float | None = None

class ChatRequest(BaseModel):
    message: str
    context_ids: List[str] = []
    chat_history: List[dict] = []

@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        result = await document_service.process_document(file)
        return {"message": "Document processed successfully", "document_id": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Generate a response based on uploaded documents"""
    try:
        response = await chat_service.generate_response(
            message=request.message,
            context_ids=request.context_ids,
            chat_history=request.chat_history
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/config")
async def update_config(config: ModelConfig):
    """Update model configuration"""
    try:
        # Update the chat service configuration
        if config.model:
            chat_service.llm.model_name = config.model
        if config.temperature is not None:
            chat_service.llm.temperature = config.temperature
        if config.max_tokens is not None:
            chat_service.llm.max_tokens = config.max_tokens
        if config.top_p is not None:
            chat_service.llm.top_p = config.top_p
        if config.frequency_penalty is not None:
            chat_service.llm.frequency_penalty = config.frequency_penalty
            
        return {"message": "Configuration updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/config")
async def get_config():
    """Get current model configuration"""
    return {
        "model": chat_service.llm.model_name,
        "temperature": chat_service.llm.temperature,
        "max_tokens": chat_service.llm.max_tokens,
        "top_p": chat_service.llm.top_p,
        "frequency_penalty": chat_service.llm.frequency_penalty
    }

@app.get("/")
async def root():
    return {"message": "Welcome to DocuChat API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 