from typing import List
from uuid import UUID

import pymongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from store.core.exception import GenericException, NotFoundException
from store.database.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import (
    ProductIn,
    ProductOut,
    ProductUpdateIn,
    ProductUpdateOut,
)


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get_client()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        try:
            # Create a 'ProductModel' instance using data from 'ProductIn'
            product_model = ProductModel(**body.model_dump())

            # Insert the serialized data of the product into the collection
            await self.collection.insert_one(product_model.model_dump())

        except Exception as exc:
            # If any exception occurs during the process, raise a 'GenericException'
            raise GenericException(
                message="Exception occurred while creating a product",
                from_exception=type(exc),
                kwargs={"class": self.__class__.__name__},
            )

        # Return a 'ProductOut' instance based on the 'product_model' data
        return ProductOut(**product_model.model_dump())

    async def get_by_id(self, id: UUID) -> ProductOut:
        try:
            # Search for a document in the collection where 'id' matches the given UUID
            result = await self.collection.find_one({"id": id})

        except Exception as exc:
            # If any exception occurs during the process, raise a 'GenericException'
            raise GenericException(
                message="Exception occurred while getting a product",
                from_exception=type(exc),
                kwargs={"class": self.__class__.__name__},
            )

        # If no document was found matching the given UUID, raise a 'NotFoundException'
        if not result:
            raise NotFoundException(
                message=f"Product not found with filter: UUID('{id}')"
            )

        # Return a 'ProductOut' instance based on the 'result' data
        return ProductOut(**result)

    async def get_all(self) -> List[ProductOut]:
        try:
            # Retrieve all documents from the collection and create a 'ProductOut' instance for each
            result = [ProductOut(**item) async for item in self.collection.find()]

        except Exception as exc:
            # If any exception occurs during the process, raise a 'GenericException'
            raise GenericException(
                message="Exception occurred while getting products",
                from_exception=type(exc),
                kwargs={"class": self.__class__.__name__},
            )

        # If no products are found, raise a 'NotFoundException'
        if not result:
            raise NotFoundException(message="No products found in the database")

        # Return the list of 'ProductOut' instances representing all retrieved products
        return result

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
