from pymongo import MongoClient

try:
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    
    # Get database list
    dbs = client.list_database_names()
    print("Connected successfully!")
    print("Available databases:", dbs)
    
    # Try to access your specific database
    db = client['docuchat']
    print("Collections in docuchat:", db.list_collection_names())
    
except Exception as e:
    print("Error connecting to MongoDB:", e) 