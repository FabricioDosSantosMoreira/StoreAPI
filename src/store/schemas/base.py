from datetime import datetime
from decimal import Decimal
from bson import Decimal128
from pydantic import BaseModel,model_validator
from pydantic_settings import SettingsConfigDict
from store.core.config import settings


class BaseSchemaMixin(BaseModel):

    model_config = SettingsConfigDict(
        arbitrary_types_allowed=True, 
        from_attributes=True
    )


class InMixin():
    @model_validator(mode="before")
    def set_schema(cls, data):
        for key, value in data.items():
            if isinstance(value, Decimal):
                data[key] = Decimal128(str(value))

        return data


class OutMixin():
    @model_validator(mode="before")
    def set_schema(cls, data):
        for key, value in data.items():
            if isinstance(value, Decimal128):
                data[key] = Decimal(str(value))
            if isinstance(value, datetime):
                data[key] = datetime.astimezone(value, settings.LOCAL_TIMEZONE)     

        return data
    