import os
from datetime import datetime
from typing import List, Dict
from fastapi import UploadFile
from bson import ObjectId
from ..db.mongodb import db
import PyPDF2
import io

DOCUMENTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "documents")

class DocumentService:
    def __init__(self):
        # Ensure documents directory exists
        os.makedirs(DOCUMENTS_DIR, exist_ok=True)

    async def store_document(self, file: UploadFile) -> Dict:
        """Store document file and metadata"""
        # Create unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(DOCUMENTS_DIR, filename)

        # Read and process the file content
        content = await file.read()
        text_content = ""
        
        if file.content_type == "application/pdf":
            # Process PDF file
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text_content = "\n".join(
                page.extract_text() for page in pdf_reader.pages
            )
        else:
            # Process text file
            text_content = content.decode('utf-8', errors='ignore')

        # Save file
        with open(file_path, "wb") as f:
            f.write(content)

        # Store metadata in database
        document = {
            "title": file.filename,
            "file_path": file_path,
            "file_type": file.content_type,
            "content": text_content,  # Store the extracted text
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "status": "processed"
        }

        result = await db.get_db().documents.insert_one(document)
        document["id"] = str(result.inserted_id)

        return document

    async def list_documents(self) -> List[Dict]:
        """List all documents"""
        cursor = db.get_db().documents.find()
        documents = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            documents.append(doc)
        return documents

    async def get_document(self, document_id: str) -> Dict:
        """Get document by ID"""
        doc = await db.get_db().documents.find_one({"_id": ObjectId(document_id)})
        if doc:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
        return doc

    def get_document_path(self, filename: str) -> str:
        """Get full path for a document"""
        return os.path.join(DOCUMENTS_DIR, filename)

document_service = DocumentService() 