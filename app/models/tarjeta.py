# app/models/tarjeta.py
from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional

class Tarjeta(Document):
    cliente_id: str
    pan_masked: str
    last4: str
    bin: str
    descripcion: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "tarjetas"
        use_state_management = True

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "cliente_id": "550e8400-e29b-41d4-a716-446655440000",
                "pan_masked": "************1234",
                "last4": "1234",
                "bin": "411111",
                "descripcion": "Tarjeta de crédito personal"
            }
        }