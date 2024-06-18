from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo


from store.models.product import ProductModel
from store.database.mongo import db_client
from store.schemas.product import (
    ProductIn,
    ProductOut,
    ProductUpdateIn,
    ProductUpdateOut,
)
from store.core.exception import NotFoundException


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get_client()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        await self.collection.insert_one(product_model.model_dump())

        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(
                message=f"Product not found with filter: UUID('{id}')"
            )

        return ProductOut(**result)

    async def query(self) -> List[ProductOut]:
        return [ProductOut(**item) async for item in self.collection.find()]

    async def update(self, id: UUID, body: ProductUpdateIn) -> ProductUpdateOut:
        # product = ProductUpdateIn(**body.model_dump(exclude_none=True))
        product = body

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": product.model_dump(exclude_none=True)},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one(filter={"id": id})
        if not product:
            raise NotFoundException(
                message=f"Product not found with filter: UUID('{id}')"
            )

        result = await self.collection.delete_one(
            filter={"id": id},
        )
        return True if result.deleted_count > 0 else False


product_usecase = ProductUsecase()
