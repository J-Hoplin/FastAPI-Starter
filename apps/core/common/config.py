from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Boost"
    DEBUG: bool = False
    DATABASE_URL: str = "mysql+aiomysql://hoplin:hoplin@localhost:3306/fastapi_db"
    REDIS_URL: Optional[str] = None
    JWT_ISSUER: str
    JWT_SECRET_KEY: str = "SECRET"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTE: int = 120
    ADMIN_SESSION_SECRET_KEY: str

    # Ignore extra fields: https://docs.pydantic.dev/2.10/api/config/#pydantic.config.ConfigDict.extra
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
