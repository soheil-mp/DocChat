from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

    async def connect_to_database(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DB_NAME]
        print("Connected to MongoDB!")

    async def close_database_connection(self):
        if self.client:
            self.client.close()
            print("Closed MongoDB connection!")

    def get_db(self):
        return self.db

db = MongoDB()