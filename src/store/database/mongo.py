from motor.motor_asyncio import AsyncIOMotorClient
from store.core.config import settings


class MongoClientWrapper:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(
            settings.DATABASE_URL, uuidRepresentation="standard"
        )
        self.db = self.client.get_database()

    def get_client(self) -> AsyncIOMotorClient:
        return self.client

    def get_database(self, db_name=None):
        if db_name:
            return self.client[db_name]
        return self.db


db_client = MongoClientWrapper()
