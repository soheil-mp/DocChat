from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import logging
import asyncio
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None

    async def connect(self, max_attempts=3, retry_delay=1):
        """Connect to MongoDB with retry logic"""
        mongodb_url = settings.MONGODB_URL
        
        for attempt in range(max_attempts):
            try:
                logger.info(f"Attempting to connect to MongoDB at {mongodb_url} (Attempt {attempt + 1}/{max_attempts})")
                self.client = AsyncIOMotorClient(mongodb_url)
                # Verify connection
                await self.client.admin.command('ping')
                self.db = self.client.get_database(settings.DB_NAME)
                logger.info("Successfully connected to MongoDB")
                logger.info(f"Using database: {self.db.name}")
                
                # Create indexes
                await self.create_indexes()
                logger.info("Database indexes created successfully")
                return
                
            except ConnectionFailure as e:
                logger.error(f"Failed to connect to MongoDB (Attempt {attempt + 1}/{max_attempts}): {str(e)}")
                if attempt < max_attempts - 1:
                    await asyncio.sleep(retry_delay)
                else:
                    raise ConnectionError("Failed to connect to MongoDB after multiple attempts")

    async def create_indexes(self):
        """Create necessary indexes for collections"""
        # Messages collection
        await self.db.messages.create_index([("session_id", 1)])
        await self.db.messages.create_index([("created_at", -1)])
        
        # Sessions collection
        await self.db.sessions.create_index([("user_id", 1)])
        await self.db.sessions.create_index([("created_at", -1)])
        
        # Documents collection
        await self.db.documents.create_index([("user_id", 1)])
        await self.db.documents.create_index([("created_at", -1)])
        await self.db.documents.create_index([("title", "text")])

    async def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("Closed MongoDB connection")

# Create a global instance
db = MongoDB()