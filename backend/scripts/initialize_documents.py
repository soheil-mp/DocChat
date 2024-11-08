import asyncio
import os
import sys
from pathlib import Path
import PyPDF2
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from app.core.config import settings
from app.services.rag_service import rag_service

async def initialize_documents():
    print("\nInitializing documents...")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    
    documents_dir = settings.DOCUMENTS_DIR
    
    for filename in os.listdir(documents_dir):
        if filename.endswith('.pdf'):
            file_path = os.path.join(documents_dir, filename)
            
            try:
                # Extract text from PDF
                with open(file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    text_content = "\n".join(
                        page.extract_text() for page in pdf_reader.pages
                    )
                
                print(f"\nProcessing: {filename}")
                print(f"Extracted {len(text_content)} characters of text")
                
                # Create document in MongoDB
                document = {
                    "title": filename,
                    "file_path": str(file_path),
                    "file_type": "application/pdf",
                    "content": text_content,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                    "status": "processed"
                }
                
                # Insert into MongoDB
                result = await db.documents.insert_one(document)
                document_id = str(result.inserted_id)
                print(f"Created MongoDB document with ID: {document_id}")
                
                # Process for RAG
                await rag_service.process_document(
                    content=text_content,
                    metadata={
                        "id": document_id,
                        "title": filename,
                        "file_path": str(file_path)
                    }
                )
                
                print(f"Successfully processed document: {filename}")
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
    
    # Close MongoDB connection
    client.close()

if __name__ == "__main__":
    asyncio.run(initialize_documents()) 