from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, StreamingResponse, Response
from typing import List
from ....services.rag_service import rag_service
from ....services.document_service import document_service
from ....models.document import DocumentResponse
import io
import mimetypes
import os

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a document for RAG
    """
    try:
        # Store document
        document = await document_service.store_document(file)
        
        # Read content with proper encoding
        content = await file.read()
        text_content = content.decode('utf-8', errors='ignore')
        
        # Process for RAG
        await rag_service.process_document(
            content=text_content,
            metadata={
                "id": document["id"],
                "title": document["title"],
                "file_path": document["file_path"]
            }
        )
        
        return {"message": "Document processed successfully", "document": document}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )

@router.get("/", response_model=List[DocumentResponse])
async def get_documents():
    """
    Get all documents
    """
    try:
        documents = await document_service.list_documents()
        print("Retrieved documents:", documents)  # Debug log
        return documents
    except Exception as e:
        print("Error getting documents:", str(e))  # Debug log
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get documents: {str(e)}"
        )

@router.get("/{document_id}")
async def get_document(document_id: str):
    """
    Get document by ID
    """
    try:
        document = await document_service.get_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{document_id}")
async def download_document(document_id: str):
    """
    Download a document
    """
    try:
        document = await document_service.get_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return FileResponse(
            document["file_path"],
            filename=document["title"],
            media_type=document["file_type"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/preview/{document_id}")
async def preview_document(document_id: str):
    """
    Preview a document (especially PDFs)
    """
    try:
        document = await document_service.get_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        file_path = document["file_path"]
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Get the correct mime type
        mime_type, _ = mimetypes.guess_type(file_path)
        
        # Return the file with appropriate headers for PDF preview
        return FileResponse(
            path=file_path,
            media_type=mime_type or 'application/octet-stream',
            filename=document["title"],
            headers={
                "Content-Disposition": f"inline; filename={document['title']}",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/debug/connection")
async def debug_connection():
    """
    Debug endpoint to check MongoDB connection
    """
    try:
        # Try to list all documents to test connection
        documents = await document_service.list_documents()
        return {
            "status": "connected",
            "document_count": len(documents),
            "documents": documents
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "type": str(type(e))
        }