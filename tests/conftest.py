# tests/conftest.py
import pytest
import asyncio
import pytest_asyncio
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.main import app
from app.models.cliente import Cliente
from app.models.tarjeta import Tarjeta
from app.core.config import settings

# Use a unique test database name
TEST_DB_NAME = "test_db_crud"

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    """Initialize test database and collections."""
    # Use the MongoDB service name from docker-compose
    test_mongodb_url = "mongodb://mongodb:27017"
    
    # Create a new client with a new event loop
    client = AsyncIOMotorClient(test_mongodb_url)
    
    # Drop test database if it exists
    await client.drop_database(TEST_DB_NAME)
    
    # Initialize Beanie with the new client
    await init_beanie(
        database=client[TEST_DB_NAME],
        document_models=[Cliente, Tarjeta]
    )
    
    # Store the client in the app state
    app.state.mongodb_client = client
    app.state.database = client[TEST_DB_NAME]
    
    # Create indexes
    await Cliente.get_motor_collection().create_index("email", unique=True)
    await Cliente.get_motor_collection().create_index("telefono", unique=True)
    await Tarjeta.get_motor_collection().create_index("pan", unique=True)
    
    yield client[TEST_DB_NAME]
    
    # Clean up
    await client.drop_database(TEST_DB_NAME)
    client.close()

@pytest.fixture
async def client(setup_db):
    """Create a test client that depends on the database setup."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def test_cliente():
    """Create a test client instance."""
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
    """Create a test tarjeta instance."""
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