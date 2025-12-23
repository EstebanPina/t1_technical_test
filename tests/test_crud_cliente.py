import pytest_asyncio
from app.crud import crud_cliente
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate

class TestCRUDCliente:

    @pytest_asyncio.fixture(autouse=True)
    async def setup_test(self, setup_db):
        await Cliente.find_all().delete()

    async def test_create_cliente(self):
        cliente_in = ClienteCreate(
            nombre="Juan Pérez",
            email="juan@example.com",
            telefono="+1234567890"
        )

        cliente = await crud_cliente.cliente.create(obj_in=cliente_in)

        assert cliente.nombre == "Juan Pérez"
        assert cliente.email == "juan@example.com"
        assert cliente.telefono == "+1234567890"

    async def test_get_cliente(self, test_cliente):
        cliente = await crud_cliente.cliente.get(id=test_cliente.id)
        assert cliente.id == test_cliente.id
