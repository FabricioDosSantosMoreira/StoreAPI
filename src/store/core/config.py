from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "StoreAPI"
    ROOT_PATH: str = ""
    DATABASE_URL: str = "mongodb://localhost:27017/store"


settings = Settings()
