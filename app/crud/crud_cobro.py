# app/crud/crud_cobro.py
from typing import Optional, List
from datetime import datetime, timedelta
from beanie.odm.queries.find import FindMany

from app.crud.base import CRUDBase
from app.models.cobro import Cobro, EstadoCobro
from app.schemas.cobro import CobroCreate, CobroUpdate

class CRUDCobro(CRUDBase[Cobro, CobroCreate, CobroUpdate]):
    async def get_by_cliente(
        self, 
        cliente_id: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Cobro]:
        return await self.model.find(
            self.model.cliente_id == cliente_id
        ).sort(-self.model.fecha_intento).skip(skip).limit(limit).to_list()
    
    async def get_by_tarjeta(
        self, 
        tarjeta_id: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Cobro]:
        return await self.model.find(
            self.model.tarjeta_id == tarjeta_id
        ).sort(-self.model.fecha_intento).skip(skip).limit(limit).to_list()
    
    async def get_by_estado(
        self, 
        estado: EstadoCobro, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Cobro]:
        return await self.model.find(
            self.model.estado == estado
        ).sort(-self.model.fecha_intento).skip(skip).limit(limit).to_list()
    
    async def get_pendientes_por_vencer(
        self, 
        dias: int = 1
    ) -> List[Cobro]:
        fecha_limite = datetime.utcnow() + timedelta(days=dias)
        return await self.model.find(
            (self.model.estado == EstadoCobro.PENDIENTE) &
            (self.model.fecha_vencimiento <= fecha_limite)
        ).to_list()
    
    async def aprobar_cobro(
        self,
        db_obj: Cobro,
        mensaje: str = "Cobro aprobado exitosamente"
    ) -> Cobro:
        db_obj.estado = EstadoCobro.APROBADO
        db_obj.mensaje_estado = mensaje
        db_obj.fecha_aprobacion = datetime.utcnow()
        await db_obj.save()
        return db_obj
    
    async def rechazar_cobro(
        self,
        db_obj: Cobro,
        motivo: str = "Cobro rechazado"
    ) -> Cobro:
        db_obj.estado = EstadoCobro.RECHAZADO
        db_obj.mensaje_estado = motivo
        db_obj.motivo_rechazo = motivo
        db_obj.fecha_rechazo = datetime.utcnow()
        await db_obj.save()
        return db_obj
    
    async def reembolsar_cobro(
        self,
        db_obj: Cobro,
        motivo: str = "Reembolso solicitado"
    ) -> Cobro:
        if db_obj.estado != EstadoCobro.APROBADO:
            raise ValueError("Solo se pueden reembolsar cobros aprobados")
        
        db_obj.estado = EstadoCobro.REEMBOLSADO
        db_obj.mensaje_estado = motivo
        db_obj.reembolsado = True
        db_obj.fecha_reembolso = datetime.utcnow()
        await db_obj.save()
        return db_obj

cobro = CRUDCobro(Cobro)