# app/crud/crud_cliente.py
from .base import CRUDBase
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate

class CRUDCliente(CRUDBase[Cliente, ClienteCreate, ClienteUpdate]):
    pass

cliente = CRUDCliente(Cliente)