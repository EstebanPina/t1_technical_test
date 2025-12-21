# app/schemas/tarjeta.py
from pydantic import BaseModel, Field, validator
from typing import Optional
from uuid import UUID
from .base import BaseSchema

class TarjetaBase(BaseSchema):
    cliente_id: UUID
    pan_masked: str = Field(..., description="Número de tarjeta enmascarado (ej. ************1234)")
    last4: str = Field(..., min_length=4, max_length=4, description="Últimos 4 dígitos de la tarjeta")
    bin: str = Field(..., min_length=6, max_length=6, description="Primeros 6 dígitos de la tarjeta (BIN)")
    descripcion: Optional[str] = None

class TarjetaCreate(BaseModel):
    cliente_id: UUID
    pan: str = Field(..., description="Número de tarjeta completo (sin espacios ni guiones)")
    descripcion: Optional[str] = None

    @validator('pan')
    def validate_pan(cls, v):
        # Remove any non-digit characters
        pan = ''.join(filter(str.isdigit, v))
        # Basic validation for PAN length (13-19 digits)
        if not (13 <= len(pan) <= 19):
            raise ValueError("El número de tarjeta debe tener entre 13 y 19 dígitos")
        return pan

class TarjetaUpdate(BaseModel):
    descripcion: Optional[str] = None
    is_active: Optional[bool] = None

class TarjetaInDB(TarjetaBase):
    id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class Tarjeta(TarjetaInDB):
    pass