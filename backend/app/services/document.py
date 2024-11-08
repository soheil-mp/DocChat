import os
from typing import List, Optional, Union, BinaryIO
from fastapi import UploadFile, HTTPException
from datetime import datetime, UTC
from bson import ObjectId
from app.db.mongodb import db
from app.models.document import Document, DocumentCreate, DocumentStatus
from app.services.vector_store import vector_store_service

ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

class DocumentService:
    def __init__(self, db_connection=None):
        self.db = db_connection or db  # Allow dependency injection for testing

    async def create_document(self, file: Union[UploadFile, BinaryIO], user_id: str) -> Document:
        # Handle different file types
        if isinstance(file, UploadFile):
            filename = file.filename
            file_ext = os.path.splitext(filename)[1].lower()
            file_content = await file.read()
        elif hasattr(file, 'read'):  # More generic file-like object check
            filename = getattr(file, 'name', 'unknown')
            file_ext = os.path.splitext(filename)[1].lower()
            file_content = file.read()
        else:
            raise ValueError("Unsupported file type")
        
        # Validate file extension
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # Validate file size
        file_size = 0
        file_size = len(file_content)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum limit of {MAX_FILE_SIZE/1024/1024}MB"
            )
        
        # Create upload directory if it doesn't exist
        upload_dir = f"uploads/{user_id}"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file
        file_path = f"{upload_dir}/{filename}"
        with open(file_path, "wb") as f:
            f.write(file_content)

        # Create document in database
        document = DocumentCreate(
            title=filename,
            file_type=file_ext,
            user_id=user_id,
            file_path=file_path
        )
        
        doc_dict = document.dict()
        doc_dict["created_at"] = datetime.now(UTC)
        doc_dict["updated_at"] = datetime.now(UTC)
        doc_dict["status"] = DocumentStatus.PENDING
        
        result = await self.db.get_db().documents.insert_one(doc_dict)
        doc_dict["id"] = str(result.inserted_id)
        
        # Start async processing of document
        await self.process_document(doc_dict["id"])
        
        return Document(**doc_dict)

    async def get_documents(self, user_id: str, skip: int = 0, limit: int = 10) -> List[Document]:
        cursor = self.db.get_db().documents.find({"user_id": user_id})
        cursor.skip(skip).limit(limit).sort("created_at", -1)
        
        documents = []
        async for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            documents.append(Document(**doc))
        
        return documents

    async def get_document(self, document_id: str, user_id: str) -> Optional[Document]:
        doc = await self.db.get_db().documents.find_one({
            "_id": ObjectId(document_id),
            "user_id": user_id
        })
        
        if not doc:
            return None
            
        doc["id"] = str(doc.pop("_id"))
        return Document(**doc)

    async def delete_document(self, document_id: str, user_id: str) -> bool:
        # Get document to check if it exists and belongs to user
        document = await self.get_document(document_id, user_id)
        if not document:
            return False
            
        # Delete file
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
            
        # Delete vector embeddings
        if document.vector_ids:
            await vector_store_service.delete_vectors(document.vector_ids)
            
        # Delete from database
        result = await self.db.get_db().documents.delete_one({
            "_id": ObjectId(document_id),
            "user_id": user_id
        })
        
        return result.deleted_count > 0

    async def process_document(self, document_id: str) -> bool:
        """Process document and create vector embeddings"""
        # Get document
        doc = await self.db.get_db().documents.find_one({"_id": ObjectId(document_id)})
        if not doc:
            return False
            
        try:
            # Update status to processing
            await self.db.get_db().documents.update_one(
                {"_id": ObjectId(document_id)},
                {"$set": {"status": DocumentStatus.PROCESSING}}
            )
            
            # Process document and get vector IDs
            vector_ids = await vector_store_service.process_document(
                file_path=doc["file_path"],
                document_id=document_id,
                metadata={
                    "title": doc["title"],
                    "user_id": doc["user_id"],
                    "file_type": doc["file_type"]
                }
            )
            
            # Update document with vector IDs and status
            await self.db.get_db().documents.update_one(
                {"_id": ObjectId(document_id)},
                {
                    "$set": {
                        "status": DocumentStatus.COMPLETED,
                        "vector_ids": vector_ids,
                        "updated_at": datetime.now(UTC)
                    }
                }
            )
            
            return True
            
        except Exception as e:
            # Update status to failed
            await self.db.get_db().documents.update_one(
                {"_id": ObjectId(document_id)},
                {
                    "$set": {
                        "status": DocumentStatus.FAILED,
                        "error": str(e),
                        "updated_at": datetime.now(UTC)
                    }
                }
            )
            return False

document_service = DocumentService() 