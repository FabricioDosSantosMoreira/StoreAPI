from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "StoreAPI"
    ROOT_PATH: Path = Path("/")

    DATABASE_URL: str = "mongodb://localhost:27017"

    model_config = SettingsConfigDict(env_file=".env")
    # DATABASE_URL=mongodb://seu_usuario:sua_senha@host:porta/nome_do_banco


settings = Settings()
