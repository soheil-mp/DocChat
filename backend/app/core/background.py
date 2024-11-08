from typing import List
import asyncio
from datetime import datetime, timedelta
from app.db.mongodb import db
from app.models.document import DocumentStatus
from app.services.document_processor import document_processor
from bson import ObjectId
import os

class BackgroundTaskManager:
    def __init__(self):
        self._processing_queue = asyncio.Queue()
        self._is_running = False

    async def start(self):
        """Start the background task processor"""
        if self._is_running:
            return
            
        self._is_running = True
        asyncio.create_task(self._process_queue())
        asyncio.create_task(self._cleanup_old_documents())

    async def stop(self):
        """Stop the background task processor"""
        self._is_running = False

    async def add_task(self, document_id: str):
        """Add a document to the processing queue"""
        await self._processing_queue.put(document_id)

    async def _process_queue(self):
        """Process documents in the queue"""
        semaphore = asyncio.Semaphore(5)  # Limit to 5 concurrent tasks
        
        while self._is_running:
            try:
                async with semaphore:
                    document_id = await self._processing_queue.get()
                    await document_processor.process_document(document_id)
            except Exception as e:
                logger.error(f"Background task error: {e}")
            finally:
                self._processing_queue.task_done()

    async def _cleanup_old_documents(self):
        """Cleanup old failed documents and temporary files"""
        while self._is_running:
            try:
                # Find old failed documents
                cutoff_date = datetime.utcnow() - timedelta(days=7)
                cursor = db.db.documents.find({
                    "status": DocumentStatus.FAILED,
                    "updated_at": {"$lt": cutoff_date}
                })
                
                async for doc in cursor:
                    # Delete associated files and records
                    document_id = str(doc["_id"])
                    await self._cleanup_document(document_id)
                
            except Exception as e:
                print(f"Error in cleanup task: {str(e)}")
            
            # Run cleanup every 24 hours
            await asyncio.sleep(86400)

    async def _cleanup_document(self, document_id: str):
        """Clean up all resources associated with a document"""
        # Delete chunks
        await db.db.document_chunks.delete_many({"document_id": document_id})
        
        # Delete vectors
        from app.services.vector_store import vector_store_service
        doc = await db.db.documents.find_one({"_id": ObjectId(document_id)})
        if doc and "vector_ids" in doc:
            await vector_store_service.delete_vectors(doc["vector_ids"])
        
        # Delete document record
        await db.db.documents.delete_one({"_id": ObjectId(document_id)})
        
        # Delete file if exists
        if doc and "file_path" in doc:
            try:
                os.remove(doc["file_path"])
            except OSError:
                pass

background_task_manager = BackgroundTaskManager() 