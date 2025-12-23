# app/models/cliente.py
from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional
from uuid import uuid4

class Cliente(Document):
    cliente_id: str = Field(default_factory=lambda: str(uuid4()), unique=True)
    nombre: str
    email: str
    telefono: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "clientes"
        use_state_management = True

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "cliente_id": "550e8400-e29b-41d4-a716-446655440000",
                "nombre": "Juan Pérez",
                "email": "juan@example.com",
                "telefono": "+5491123456789"
            }
        }