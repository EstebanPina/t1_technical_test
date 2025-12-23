# app/schemas/tarjeta.py
from datetime import datetime
from pydantic import BaseModel, Field, validator, ConfigDict
from typing import Optional, List, Any
from uuid import UUID
from bson import ObjectId
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
    id: Any
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        },
        arbitrary_types_allowed=True
    )
    @validator('id')
    def validate_id(cls, v):
        # Convierte ObjectId a string
        if hasattr(v, 'id'):
            return str(v.id)
        return str(v)
class TarjetaGenerateRequest(BaseModel):
    bin: str
    count: int = Field(1, ge=1, le=50, description="Número de tarjetas a generar (máx. 50)")
    length: int = Field(16, ge=13, le=19, description="Longitud de la tarjeta (13-19)")
class TarjetaGenerateResponse(BaseModel):
    cards: List[str]
    bin: str
    length: int
class Tarjeta(TarjetaInDB):
    pass
