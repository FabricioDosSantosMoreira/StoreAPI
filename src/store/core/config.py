from pydantic_settings import BaseSettings

from pytz import timezone
from pytz.tzinfo import BaseTzInfo

class Settings(BaseSettings):

    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: str = "27017"
    DATABASE_NAME: str = "store"
    DATABASE_PRODUCT_COLLECTION: str = "products"

    DATABASE_URL: str = f"mongodb://{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

    PROJECT_NAME: str = "MongoDB-StoreAPI"
    ROOT_PATH: str = ""
    
    LOCAL_TIMEZONE: BaseTzInfo = timezone('America/Sao_Paulo')
    UTC_TIMEZONE: BaseTzInfo  = timezone('UTC')

settings = Settings()
