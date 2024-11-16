from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, StreamingResponse, Response
from typing import List
from ....services.rag_service import rag_service
from ....services.document_service import document_service
from ....models.document import DocumentResponse
import io
import mimetypes
import os
import PyPDF2

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a document for RAG
    """
    try:
        # Store document
        document = await document_service.store_document(file)
        
        # Convert ObjectId to string for JSON serialization
        if "_id" in document:
            document["id"] = str(document["_id"])
            del document["_id"]
        
        # Extract text from PDF
        if file.filename.endswith('.pdf'):
            # Reset file pointer
            await file.seek(0)
            content = await file.read()
            
            # Use PyPDF2 to extract text
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text_content = "\n".join(
                page.extract_text() for page in pdf_reader.pages
            )
        else:
            # For non-PDF files, try basic text extraction
            await file.seek(0)
            content = await file.read()
            text_content = content.decode('utf-8', errors='ignore')
        
        # Process document with RAG
        await rag_service.process_document(
            content=text_content,
            metadata={
                "id": document["id"],
                "title": document["title"],
                "file_path": document["file_path"],
                "file_type": document.get("file_type", "application/octet-stream")
            }
        )
        
        return {"message": "Document processed successfully", "document": document}
    except Exception as e:
        print(f"Upload error: {str(e)}")  # Add logging
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

@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """Delete a document and its vectors from both MongoDB and Pinecone"""
    try:
        await document_service.initialize()  # Make sure service is initialized
        
        # First, delete from MongoDB
        result = await document_service.delete_document(document_id)
        if not result:
            raise HTTPException(status_code=404, detail="Document not found")
            
        # Then, delete from Pinecone
        try:
            # Delete vectors with matching document_id from Pinecone
            await rag_service.delete_document_vectors(document_id)
        except Exception as e:
            logger.error(f"Error deleting vectors for document {document_id}: {str(e)}")
            # Even if Pinecone deletion fails, we've already deleted from MongoDB
            
        return {"message": "Document deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))