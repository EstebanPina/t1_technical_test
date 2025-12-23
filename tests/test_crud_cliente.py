import pytest
from uuid import uuid4
from app.crud import crud_cliente
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate

@pytest.mark.anyio
class TestCRUDCliente:
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
        assert cliente.nombre == test_cliente.nombre
    
    async def test_get_by_email(self, test_cliente):
        # Get cliente by email
        cliente = await crud_cliente.cliente.get_by_email(test_cliente.email)
        
        # Assertions
        assert cliente is not None
        assert cliente.email == test_cliente.email
    
    async def test_get_by_telefono(self, test_cliente):
        # Get cliente by telefono
        cliente = await crud_cliente.cliente.get_by_telefono(test_cliente.telefono)
        
        # Assertions
        assert cliente is not None
        assert cliente.telefono == test_cliente.telefono
    
    async def test_update_cliente(self, test_cliente):
        # Update data
        update_data = {"nombre": "Nombre Actualizado"}
        cliente_updated = await crud_cliente.cliente.update(
            db_obj=test_cliente, 
            obj_in=ClienteUpdate(**update_data)
        )
        
        # Assertions
        assert cliente_updated.nombre == update_data["nombre"]
        assert cliente_updated.email == test_cliente.email
    
    async def test_delete_cliente(self, test_cliente):
        # Delete cliente
        deleted = await crud_cliente.cliente.remove(id=test_cliente.id)
        
        # Try to get deleted cliente
        cliente = await crud_cliente.cliente.get(id=test_cliente.id)
        
        # Assertions
        assert deleted is True
        assert cliente is None
