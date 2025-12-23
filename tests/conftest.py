import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.main import app
from app.models.cliente import Cliente
from app.models.tarjeta import Tarjeta

TEST_DB_NAME = "test_db_crud"


# =========================================================
# Inicialización de DB (UN LOOP = UN TEST)
# =========================================================
@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db():
    client = AsyncIOMotorClient("mongodb://mongodb:27017")

    # Base limpia por test
    await client.drop_database(TEST_DB_NAME)

    await init_beanie(
        database=client[TEST_DB_NAME],
        document_models=[Cliente, Tarjeta],
    )

    yield

    await client.drop_database(TEST_DB_NAME)
    client.close()


# =========================================================
# Cliente FastAPI (SIN lifespan)
# =========================================================
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app, lifespan="off")
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# =========================================================
# Fixtures de datos
# =========================================================
@pytest_asyncio.fixture
async def test_cliente():
    cliente = Cliente(
        nombre="Test Cliente",
        email="test@example.com",
        telefono="+1234567890",
    )
    await cliente.create()
    return cliente


@pytest_asyncio.fixture
async def test_tarjeta(test_cliente):
    tarjeta = Tarjeta(
        cliente_id=str(test_cliente.id),
        pan="4111111111111111",
        pan_masked="************1111",
        last4="1111",
        bin="411111",
        descripcion="Tarjeta de prueba",
    )
    await tarjeta.create()
    return tarjeta
