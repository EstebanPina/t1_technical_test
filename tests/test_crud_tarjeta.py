import pytest
from app.crud import crud_tarjeta
from app.schemas.tarjeta import TarjetaCreate, TarjetaUpdate

@pytest.mark.anyio
class TestCRUDTarjeta:
    async def test_create_tarjeta(self, test_cliente):
        # Test data
        tarjeta_data = {
            "cliente_id": str(test_cliente.id),
            "pan": "5555555555554444",  # Mastercard test number
            "pan_masked": "************4444",
            "last4": "4444",
            "bin": "555555",
            "descripcion": "Tarjeta de prueba"
        }
        tarjeta_in = TarjetaCreate(**tarjeta_data)
        
        # Create tarjeta
        tarjeta = await crud_tarjeta.tarjeta.create(obj_in=tarjeta_in)
        
        # Assertions
        assert tarjeta is not None
        assert tarjeta.cliente_id == tarjeta_data["cliente_id"]
        assert tarjeta.pan_masked == tarjeta_data["pan_masked"]
        assert tarjeta.last4 == tarjeta_data["last4"]
        assert tarjeta.bin == tarjeta_data["bin"]
        assert hasattr(tarjeta, "id")
    
    async def test_get_tarjeta(self, test_tarjeta):
        # Get tarjeta by ID
        tarjeta = await crud_tarjeta.tarjeta.get(id=test_tarjeta.id)
        
        # Assertions
        assert tarjeta is not None
        assert tarjeta.id == test_tarjeta.id
        assert tarjeta.pan_masked == test_tarjeta.pan_masked
    
    async def test_get_multi_by_cliente(self, test_tarjeta):
        # Get tarjetas by cliente_id
        tarjetas = await crud_tarjeta.tarjeta.get_multi(
            cliente_id=str(test_tarjeta.cliente_id)
        )
        
        # Assertions
        assert isinstance(tarjetas, list)
        assert len(tarjetas) > 0
        assert any(t.id == test_tarjeta.id for t in tarjetas)
    
    async def test_update_tarjeta(self, test_tarjeta):
        # Update data
        update_data = {"descripcion": "Descripción actualizada"}
        tarjeta_updated = await crud_tarjeta.tarjeta.update(
            db_obj=test_tarjeta,
            obj_in=TarjetaUpdate(**update_data)
        )
        
        # Assertions
        assert tarjeta_updated.descripcion == update_data["descripcion"]
        assert tarjeta_updated.id == test_tarjeta.id
    
    async def test_delete_tarjeta(self, test_tarjeta):
        # Delete tarjeta
        deleted = await crud_tarjeta.tarjeta.remove(id=test_tarjeta.id)
        
        # Try to get deleted tarjeta
        tarjeta = await crud_tarjeta.tarjeta.get(id=test_tarjeta.id)
        
        # Assertions
        assert deleted is True
        assert tarjeta is None
