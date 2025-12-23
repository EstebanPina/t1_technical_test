# app/crud/crud_cliente.py
from typing import Optional
from .base import CRUDBase
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate

class CRUDCliente(CRUDBase[Cliente, ClienteCreate, ClienteUpdate]):
    async def get_by_email(self, email: str) -> Optional[Cliente]:
        return await self.model.find_one({"email": email})
    
    async def get_by_telefono(self, telefono: str) -> Optional[Cliente]:
        return await self.model.find_one({"telefono": telefono})

cliente = CRUDCliente(Cliente)