# app/db/init_db.py
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.models.cliente import Cliente
from app.models.tarjeta import Tarjeta

async def init_db():
    # Create Motor client
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    
    # Initialize beanie with the document models
    await init_beanie(
        database=client[settings.MONGODB_DB_NAME],  # Updated to match config
        document_models=[Cliente, Tarjeta]
    )