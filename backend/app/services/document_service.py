import os
import logging
from typing import List, Optional
from fastapi import UploadFile, HTTPException
from ..models.document import DocumentResponse
from bson import ObjectId
from ..db.mongodb import db
import PyPDF2
import io
from datetime import datetime

logger = logging.getLogger(__name__)

class DocumentService:
    def __init__(self):
        self.upload_dir = "uploads"
        self.db = None
        self.collection = None
        # Ensure upload directory exists
        os.makedirs(self.upload_dir, exist_ok=True)

    async def initialize(self):
        """Initialize database connection"""
        if self.collection is None:  # Check collection instead of db
            await db.connect_to_database()
            database = db.client['docuchat']
            self.collection = database['documents']
            logger.info("Initialized database connection and collection")

    async def list_documents(self) -> List[DocumentResponse]:
        """List all documents"""
        try:
            await self.initialize()
            # Get all documents from MongoDB using the collection
            cursor = self.collection.find()
            documents = await cursor.to_list(length=None)
            logger.info(f"Retrieved {len(documents)} documents from database")
            
            # Convert to DocumentResponse objects
            return [
                DocumentResponse(
                    id=str(doc["_id"]),
                    title=doc["title"],
                    type=doc.get("file_type", "application/octet-stream"),
                    created_at=doc.get("created_at", datetime.utcnow()),
                    path=doc.get("file_path", ""),
                    updated_at=doc.get("updated_at", datetime.utcnow())
                ) for doc in documents
            ]
        except Exception as e:
            logger.error(f"Error listing documents: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to list documents: {str(e)}"
            )

    async def store_document(self, file: UploadFile) -> dict:
        """Store a document and return its metadata"""
        try:
            await self.initialize()
            
            # Generate safe filename and save file
            filename = file.filename
            file_path = self.get_document_path(filename)
            
            # Save file content
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
                
            # Create document metadata
            document = {
                "title": filename,
                "file_path": file_path,
                "file_type": file.content_type or "application/octet-stream",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # Store in MongoDB
            result = await self.collection.insert_one(document)
            document["id"] = str(result.inserted_id)  # Convert ObjectId to string
            
            logger.info(f"Stored document: {document['title']}")
            return document
        except Exception as e:
            logger.error(f"Error storing document: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to store document: {str(e)}"
            )

    async def get_document(self, document_id: str) -> Optional[dict]:
        """Get a document by ID"""
        try:
            await self.initialize()
            document = await self.collection.find_one({"_id": ObjectId(document_id)})
            if document:
                document["id"] = str(document["_id"])
            return document
        except Exception as e:
            logger.error(f"Error getting document {document_id}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get document: {str(e)}"
            )

    def get_document_path(self, filename: str) -> str:
        """Get full path for a document"""
        return os.path.join(self.upload_dir, filename)

    async def delete_document(self, document_id: str) -> bool:
        """Delete a document by ID"""
        try:
            await self.initialize()  # Make sure we're connected to the database
            result = await self.collection.delete_one({"_id": ObjectId(document_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete document: {str(e)}"
            )

document_service = DocumentService()