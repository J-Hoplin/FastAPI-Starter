from pydantic_settings import BaseSettings,SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI RAG Template"
    DEBUG: bool = False
    DATABASE_URL: str = "mysql+pymysql://hoplin:hoplin@localhost:3306/fastapi_db"
    REDIS_URL: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
