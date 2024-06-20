from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
import pymongo
from store.core.exception import GenericException, NotFoundException
from store.database.mongo import db_client
from store.models.product import ProductCreateModel, ProductUpdateModel
from store.schemas.product import ProductIn, ProductOut, ProductCreateIn, ProductUpdateIn


class ProductUsecase():

    def __init__(self) -> None:

        self.client: AsyncIOMotorClient = db_client.client
        self.database: AsyncIOMotorDatabase = db_client.database
        
        self.collection: AsyncIOMotorCollection = db_client.product_collection


    async def create(self, body: ProductCreateIn) -> ProductOut:
        try:
            # Create a 'ProductCreateModel' instance using data from 'ProductCreateIn'
            product_model = ProductCreateModel(**body.model_dump())
            product = ProductIn(**product_model.model_dump())

            # Insert the serialized data of the product into the collection
            await self.collection.insert_one(product.model_dump())

        except Exception as exc:
            # If any exception occurs during the process, raise a 'GenericException'
            raise GenericException(
                message="Exception occurred while creating a product",
                from_exception=type(exc),
                extra={"exception": exc, "class": self.__class__.__name__},
            )

        # Return a 'ProductOut' instance based on the 'product' data
        return ProductOut(**product.model_dump())


    async def get_by_id(self, id: UUID) -> ProductOut:
        try:
            # Search for a document in the collection where 'id' matches the given UUID
            result = await self.collection.find_one({"id": id})

        except Exception as exc:
            # If any exception occurs during the process, raise a 'GenericException'
            raise GenericException(
                message="Exception occurred while getting a product",
                from_exception=type(exc),
                kwargs={"exception": exc, "class": self.__class__.__name__},
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
                kwargs={"exception": exc, "class": self.__class__.__name__},
            )

        # If no products are found, raise a 'NotFoundException'
        if not result:
            raise NotFoundException(message="No products found in the database")

        # Return the list of 'ProductOut' instances
        return result


    async def update(self, id: UUID, body: ProductUpdateIn) -> ProductOut:

        product = ProductUpdateModel(**body.model_dump())

        try:
            # Find a document with the given 'id' and update it with the new data from 'body'
            result = await self.collection.find_one_and_update(
                filter={"id": id},
                update={"$set": product.model_dump(exclude_none=True)},
                return_document=pymongo.ReturnDocument.AFTER,
            )
        except Exception as exc:
            # If any exception occurs during the process, raise a 'GenericException'
            raise GenericException(
                message="Exception occurred while updating a product",
                from_exception=type(exc),
                kwargs={"class": self.__class__.__name__}
            )
   
        # If no document was found and updated, raise a 'NotFoundException'
        if not result:
            raise NotFoundException(
                message=f"Product not found with id: UUID('{id}')"
            )
        
        # Return a 'ProductOut' instance initialized with the updated document's data
        return ProductOut(**result)


    async def delete(self, id: UUID) -> bool:
        try:
            # Search for a document in the collection where 'id' matches the given UUID
            product = await self.collection.find_one(filter={"id": id})

        except Exception as exc:
            # If any exception occurs during the process, raise a 'GenericException'
            raise GenericException(
                message="Exception occurred while getting a product to delete",
                from_exception=type(exc),
                kwargs={"exception": exc, "class": self.__class__.__name__},
            )

        # If no document was found, raise a 'NotFoundException'
        if not product:
            raise NotFoundException(
                message=f"Product not found with filter: UUID('{id}')"
            )

        try:
            # Delete a document in the collection where 'id' matches the given UUID
            result = await self.collection.delete_one(filter={"id": id})
        except Exception as exc:
            # If any exception occurs during the process, raise a 'GenericException'
            raise GenericException(
                message="Exception occurred while deleting a product",
                from_exception=type(exc),
                kwargs={"exception": exc, "class": self.__class__.__name__},
            )

        return True if result.deleted_count > 0 else False


product_usecase = ProductUsecase()
