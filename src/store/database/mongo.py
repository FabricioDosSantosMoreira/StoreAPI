from typing import Union
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from store.core.config import settings
from store.core.exception import DataBaseException


class MongoDBClientWrapper():

    def __init__(self) -> None:

        self.client: AsyncIOMotorClient = self.get_client(
            url=settings.DATABASE_URL
        )
        self.database: AsyncIOMotorDatabase = self.get_database(
            name=settings.DATABASE_NAME
        )

        self.product_collection: AsyncIOMotorCollection = self.get_collection(
            name=settings.DATABASE_PRODUCT_COLLECTION
        )


    def get_client(self, url: str) -> AsyncIOMotorClient:
        try: 
            client: AsyncIOMotorClient = AsyncIOMotorClient(
                url,
                uuidRepresentation="standard",
            )
        except Exception as exc:
            raise DataBaseException(
                message=f"Exception ocurred while getting client with url ['{url}']",
                from_exception=type(exc),
                extra={"exception": exc}
            )

        return client


    def get_database(self, name: str) -> AsyncIOMotorDatabase:
        try:
            database: AsyncIOMotorDatabase = AsyncIOMotorDatabase(
                client=self.client,
                name=name
            )
        except Exception as exc:
            raise DataBaseException(
                message=f"Exception ocurred while getting database ['{name}']",
                from_exception=type(exc),
                kwargs={"exception": exc}
            )

        return database
    

    def get_collection(self, name: str) -> Union[None, AsyncIOMotorCollection]:
        if name is None or name.isspace():
            return None

        try:
            collection = self.database.get_collection(name)
        except Exception as exc:
            raise DataBaseException(
                message=f"Exception ocurred while getting collection ['{name}']",
                from_exception=type(exc),
                kwargs={"exception": exc}
            )

        return collection
        

db_client = MongoDBClientWrapper()
