import asyncio
import os
import sys
from pathlib import Path
import PyPDF2

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from app.services.document_service import document_service
from app.services.rag_service import rag_service
from app.core.config import settings

async def process_existing_documents():
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
                
                # Create document metadata
                document = {
                    "title": filename,
                    "file_path": file_path,
                    "file_type": "application/pdf",
                    "content": text_content
                }
                
                # Process document with RAG
                await rag_service.process_document(
                    content=text_content,
                    metadata=document
                )
                
                print(f"Successfully processed: {filename}")
                print(f"Extracted {len(text_content)} characters of text")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(process_existing_documents()) 