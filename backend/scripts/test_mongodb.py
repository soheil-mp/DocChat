from pymongo import MongoClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_mongodb_connection():
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        
        # Get database list
        dbs = client.list_database_names()
        logger.info(f"Connected successfully! Available databases: {dbs}")
        
        # Try to access your specific database
        db = client['docuchat']
        collections = db.list_collection_names()
        logger.info(f"Collections in docuchat: {collections}")
        
        # Try to count documents
        doc_count = db.documents.count_documents({})
        logger.info(f"Number of documents in collection: {doc_count}")
        
        return True
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        return False

if __name__ == "__main__":
    test_mongodb_connection() 