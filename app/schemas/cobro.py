# app/schemas/cobro.py
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, UUID4
from app.models.cobro import EstadoCobro

class CobroBase(BaseModel):
    cliente_id: str = Field(..., description="ID del cliente")
    tarjeta_id: str = Field(..., description="ID de la tarjeta usada")
    monto: float = Field(..., gt=0, description="Monto del cobro")
    moneda: str = Field("MXN", description="Código de moneda (ISO 4217)")
    descripcion: str = Field(..., description="Descripción del cobro")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadatos adicionales")

class CobroCreate(CobroBase):
    pass

class CobroUpdate(BaseModel):
    estado: Optional[EstadoCobro] = None
    mensaje_estado: Optional[str] = None
    motivo_rechazo: Optional[str] = None
    reembolsado: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None

class CobroInDBBase(CobroBase):
    id: str = Field(..., alias="_id")
    estado: EstadoCobro
    mensaje_estado: Optional[str] = None
    fecha_intento: datetime
    fecha_aprobacion: Optional[datetime] = None
    fecha_rechazo: Optional[datetime] = None
    motivo_rechazo: Optional[str] = None
    reembolsado: bool = False
    fecha_reembolso: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Cobro(CobroInDBBase):
    pass

class CobroInDB(CobroInDBBase):
    pass