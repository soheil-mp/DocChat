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
        """Store a document"""
        try:
            await self.initialize()
            # Create user directory if it doesn't exist
            user_dir = os.path.join(self.upload_dir, "default_user")
            os.makedirs(user_dir, exist_ok=True)

            # Save file
            file_path = os.path.join(user_dir, file.filename)
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)

            # Create document record
            document = {
                "title": file.filename,
                "file_type": file.content_type or "text/plain",
                "file_path": file_path,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "path": file_path  # Add path field to match DocumentResponse model
            }

            # Store in MongoDB using the collection
            result = await self.collection.insert_one(document)
            document["id"] = str(result.inserted_id)
            
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

document_service = DocumentService()