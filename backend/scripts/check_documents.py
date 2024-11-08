import os
import sys
from pathlib import Path
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from app.core.config import settings

async def check_documents():
    documents_dir = settings.DOCUMENTS_DIR
    print(f"\nChecking documents directory: {documents_dir}")
    print(f"Directory exists: {os.path.exists(documents_dir)}")
    
    if os.path.exists(documents_dir):
        files = os.listdir(documents_dir)
        print(f"\nFiles found in directory:")
        for file in files:
            file_path = os.path.join(documents_dir, file)
            print(f"- {file} ({os.path.getsize(file_path)} bytes)")
    else:
        print("Documents directory does not exist!")

    # Check MongoDB
    print("\nChecking MongoDB:")
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    
    # List documents in MongoDB
    documents = await db.documents.find().to_list(length=None)
    print(f"\nDocuments in MongoDB:")
    for doc in documents:
        print(f"- {doc.get('title')} (ID: {doc.get('_id')})")
        print(f"  Path: {doc.get('file_path')}")
        print(f"  Type: {doc.get('file_type')}")
        print(f"  Status: {doc.get('status')}")
        print()

    # Close MongoDB connection
    client.close()

if __name__ == "__main__":
    asyncio.run(check_documents()) 