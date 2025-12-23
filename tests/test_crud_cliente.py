# tests/test_crud_cliente.py
import pytest
from app.crud import crud_cliente
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate

@pytest.mark.asyncio
class TestCRUDCliente:
    @pytest.fixture(autouse=True)
    async def setup_test(self, setup_db):
        """Setup test data for each test method"""
        self.db = setup_db
        # Clear any existing data
        await Cliente.find_all().delete()

    async def test_create_cliente(self):
        # Test data
        cliente_data = {
            "nombre": "Juan Pérez",
            "email": "juan@example.com",
            "telefono": "+1234567890"
        }
        cliente_in = ClienteCreate(**cliente_data)
        
        # Create cliente
        cliente = await crud_cliente.cliente.create(obj_in=cliente_in)
        
        # Assertions
        assert cliente is not None
        assert cliente.nombre == cliente_data["nombre"]
        assert cliente.email == cliente_data["email"]
        assert cliente.telefono == cliente_data["telefono"]
        assert hasattr(cliente, "id")
    
    async def test_get_cliente(self, test_cliente):
        # Get cliente by ID
        cliente = await crud_cliente.cliente.get(id=test_cliente.id)
        
        # Assertions
        assert cliente is not None
        assert cliente.id == test_cliente.id
        assert cliente.email == test_cliente.email