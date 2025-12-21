from typing import Optional
from pydantic import EmailStr, Field
from datetime import datetime
from uuid import UUID
from .base import BaseSchema, BaseCreateSchema, BaseUpdateSchema

class ClienteBase(BaseSchema):
    nombre: str
    email: EmailStr
    telefono: str

class ClienteCreate(BaseCreateSchema):
    nombre: str
    email: EmailStr
    telefono: str

class ClienteUpdate(BaseUpdateSchema):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None

class Cliente(ClienteBase):
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "nombre": "Juan Pérez",
                "email": "juan.perez@example.com",
                "telefono": "+521234567890",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        }
