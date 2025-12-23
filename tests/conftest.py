import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from datetime import datetime

from app.main import app
from app.models.cliente import Cliente
from app.models.tarjeta import Tarjeta
from app.core.config import settings

TEST_DB_NAME = "test_db"

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(autouse=True)
async def setup_db():
    # Set test database URL
    test_mongodb_url = "mongodb://localhost:27017"
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(test_mongodb_url)
    
    # Drop test database if it exists
    await client.drop_database(TEST_DB_NAME)
    
    # Initialize Beanie
    await init_beanie(
        database=client[TEST_DB_NAME],
        document_models=[Cliente, Tarjeta]
    )
    
    yield
    
    # Clean up after tests
    await client.drop_database(TEST_DB_NAME)
    client.close()

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def test_cliente():
    cliente_data = {
        "nombre": "Test Cliente",
        "email": "test@example.com",
        "telefono": "+1234567890"
    }
    cliente = Cliente(**cliente_data)
    await cliente.create()
    return cliente

@pytest.fixture
async def test_tarjeta(test_cliente):
    tarjeta_data = {
        "cliente_id": str(test_cliente.id),
        "pan": "4111111111111111",
        "pan_masked": "************1111",
        "last4": "1111",
        "bin": "411111",
        "descripcion": "Tarjeta de prueba"
    }
    tarjeta = Tarjeta(**tarjeta_data)
    await tarjeta.create()
    return tarjeta
