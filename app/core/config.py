# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "API de Pagos"
    API_V1_STR: str = "/api/v1"
    MONGODB_URL: str = "mongodb://mongodb:27017"
    MONGODB_DB_NAME: str = "fastapi_db"  # Changed from MONGO_DB to match docker-compose

    class Config:
        case_sensitive = True

settings = Settings()