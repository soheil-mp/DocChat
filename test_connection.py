from pymongo import MongoClient
import sys

def test_mongodb_connection():
    try:
        # Connect with a timeout
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        
        # Force a connection to verify
        client.admin.command('ping')
        
        print("✓ MongoDB Connection Successful!")
        
        # Get database list
        dbs = client.list_database_names()
        print("\nAvailable databases:", dbs)
        
        # Check for docuchat database
        if 'docuchat' in dbs:
            db = client['docuchat']
            collections = db.list_collection_names()
            print("\nCollections in docuchat:", collections)
        else:
            print("\nNote: 'docuchat' database not found")
            
    except Exception as e:
        print("✗ MongoDB Connection Failed!")
        print("\nError:", str(e))
        print("\nTroubleshooting tips:")
        print("1. Verify MongoDB is running (already confirmed)")
        print("2. Check if port 27017 is not blocked")
        print("3. Ensure no authentication is required (or provide credentials)")
        sys.exit(1)

if __name__ == "__main__":
    test_mongodb_connection() 