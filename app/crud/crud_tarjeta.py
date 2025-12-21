# app/crud/crud_tarjeta.py
from typing import Optional, List
from beanie.odm.queries.find import FindMany
from app.crud.base import CRUDBase
from app.models.tarjeta import Tarjeta
from app.schemas.tarjeta import TarjetaCreate, TarjetaUpdate

class CRUDTarjeta(CRUDBase[Tarjeta, TarjetaCreate, TarjetaUpdate]):
    async def create_with_owner(
        self, 
        obj_in: TarjetaCreate, 
        owner_id: str
    ) -> Tarjeta:
        # The Tarjeta model will handle the PAN masking
        db_obj = Tarjeta(
            **obj_in.dict(exclude_unset=True),
            cliente_id=owner_id
        )
        await db_obj.create()
        return db_obj

    async def get_by_cliente(
        self, 
        cliente_id: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Tarjeta]:
        return await self.model.find(
            self.model.cliente_id == cliente_id
        ).skip(skip).limit(limit).to_list()

    async def get_by_last4(
        self, 
        last4: str, 
        cliente_id: str
    ) -> Optional[Tarjeta]:
        return await self.model.find_one(
            (self.model.last4 == last4) & 
            (self.model.cliente_id == cliente_id)
        )

    async def get_by_bin(
        self, 
        bin: str, 
        cliente_id: str
    ) -> List[Tarjeta]:
        return await self.model.find(
            (self.model.bin == bin) & 
            (self.model.cliente_id == cliente_id)
        ).to_list()

tarjeta = CRUDTarjeta(Tarjeta)