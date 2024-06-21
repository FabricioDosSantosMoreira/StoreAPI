from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional
from uuid import uuid4
from bson import Decimal128
from pydantic import UUID4, Field, model_validator, root_validator
import pytz
from store.schemas.base import BaseSchemaMixin, InMixin, OutMixin
from store.core.config import settings


class ProductBase(BaseSchemaMixin):

    name: Annotated[Optional[str], Field(description="Product Name", example="Intel Core i5 2410M")]
    price: Annotated[Optional[Decimal], Field(description="Product Price", example=225.5)]
    quantity: Annotated[Optional[int], Field(description="Product Quantity", example=500)]

    status: Annotated[Optional[bool], Field(description="Product Status", example=False)]


class ProductIn(BaseSchemaMixin, InMixin):

    id: Annotated[Optional[UUID4], Field(example=uuid4())]
    status: Annotated[Optional[bool], Field(example=False)]
    
    name: Annotated[Optional[str], Field(example="Intel Core i5 2410M")]
    price: Annotated[Optional[Decimal128], Field(example=225.5)]
    quantity: Annotated[Optional[int], Field(example=500)]

    updated_at: Annotated[Optional[datetime], Field(example=datetime.now(settings.UTC_TIMEZONE))]
    created_at: Annotated[Optional[datetime], Field(example=datetime.now(settings.UTC_TIMEZONE))]    
    

class ProductOut(BaseSchemaMixin, OutMixin):

    id: Annotated[Optional[UUID4], Field(example=uuid4())]
    status: Annotated[Optional[bool], Field(example=False)]

    name: Annotated[Optional[str], Field(example="Intel Core i5 2410M")]
    price: Annotated[Optional[Decimal], Field(example=225.5)]
    quantity: Annotated[Optional[int], Field(example=500)]
   
    updated_at: Annotated[Optional[datetime], Field(example=datetime.now(settings.LOCAL_TIMEZONE))]
    created_at: Annotated[Optional[datetime], Field(example=datetime.now(settings.LOCAL_TIMEZONE))]

    
class ProductCreateIn(BaseSchemaMixin):

    name: Annotated[str, Field(description="Product Name", example="Intel Core i5 2410M")]
    price: Annotated[Decimal, Field(description="Product Price", example=225.5)]
    quantity: Annotated[int, Field(description="Product Quantity", example=500)]

    status: Annotated[bool, Field(description="Product Status", example=False)]


class ProductUpdateIn(BaseSchemaMixin):

    name: Annotated[Optional[str], Field(None, description="Product Name", example="Intel Core i5 2410M")]
    price: Annotated[Optional[Decimal], Field(None, description="Product Price", example=225.5)]
    quantity: Annotated[Optional[int], Field(None, description="Product Quantity", example=500)]

    status: Annotated[Optional[bool], Field(None, description="Product Status", example=False)]


class ProductUpdateInDatabase(BaseSchemaMixin):

    name: Optional[str] = None
    price: Optional[Decimal128] = None
    quantity: Optional[int] = None
    status: Optional[bool] = None

    updated_at: datetime = None

    @model_validator(mode="before")
    def convert_price(cls, data):
        data['price'] = Decimal128(str(data['price']))
        data['updated_at'] = datetime.now(settings.UTC_TIMEZONE)
        return data

   