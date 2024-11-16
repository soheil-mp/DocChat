from typing import Optional, List
from contextlib import AsyncExitStack
from fastapi import UploadFile
from app.models.document import Document
from app.services.vector_store import VectorStoreService
from app.core.config import settings
from app.db.mongodb import db
from bson import ObjectId
import os
import aiofiles
from datetime import datetime, timezone
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self, vector_store: Optional[VectorStoreService] = None):
        self.vector_store = vector_store
        self.chunk_size = 1000
        self.chunk_overlap = 200
        self._cache = {}

    async def get_document(self, document_id: str) -> Optional[Document]:
        """Get document with caching"""
        if document_id in self._cache:
            return self._cache[document_id]
            
        doc = await db.db.documents.find_one({"_id": ObjectId(document_id)})
        if doc:
            doc["id"] = str(doc.pop("_id"))
            self._cache[document_id] = Document(**doc)
            return self._cache[document_id]
        return None

    async def update_document_status(self, document_id: str, status: str) -> bool:
        """Update document processing status"""
        result = await db.db.documents.update_one(
            {"_id": ObjectId(document_id)},
            {
                "$set": {
                    "status": status,
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )
        return result.modified_count > 0

    async def process_document(self, document_id: str) -> bool:
        """Process a document and store its vectors"""
        try:
            # Get document from database
            document = await self.get_document(document_id)
            if not document:
                return False

            # Read document content
            content = await self.read_document_content(document.file_path)

            # Split into chunks
            chunks = self.split_text(content)

            # Create embeddings and metadata
            metadata_list = [
                {
                    "document_id": document_id,
                    "chunk_index": i,
                    "text": chunk,
                    "title": document.title
                }
                for i, chunk in enumerate(chunks)
            ]

            # Create and store vectors
            if self.vector_store:
                vectors = await self.vector_store.create_embeddings(
                    texts=chunks,
                    metadata_list=metadata_list
                )
                await self.vector_store.batch_upsert(vectors)

            # Update document status
            await self.update_document_status(document_id, "processed")
            return True

        except Exception as e:
            print(f"Error processing document {document_id}: {str(e)}")
            await self.update_document_status(document_id, "error")
            return False

    async def save_uploaded_file(self, file: UploadFile, document_id: str) -> str:
        """Save an uploaded file to disk"""
        # Create uploads directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Generate file path
        file_extension = os.path.splitext(file.filename)[1]
        file_path = os.path.join(settings.UPLOAD_DIR, f"{document_id}{file_extension}")
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
            
        return file_path

    def split_text(self, text: str) -> List[str]:
        """Optimize text splitting with better chunking"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        return text_splitter.split_text(text)

    async def read_document_content(self, file_path: str) -> str:
        """Read document content from file"""
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
            content = await file.read()
        return content

# Create global instance
document_processor = DocumentProcessor()