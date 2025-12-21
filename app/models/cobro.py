# app/models/cobro.py
from datetime import datetime
from enum import Enum
from beanie import Document
from pydantic import Field

class EstadoCobro(str, Enum):
    PENDIENTE = "pendiente"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"
    REEMBOLSADO = "reembolsado"

class Cobro(Document):
    cliente_id: str = Field(..., description="ID del cliente")
    tarjeta_id: str = Field(..., description="ID de la tarjeta usada")
    monto: float = Field(..., gt=0, description="Monto del cobro")
    moneda: str = Field(default="MXN", description="Código de moneda (ISO 4217)")
    descripcion: str = Field(..., description="Descripción del cobro")
    estado: EstadoCobro = Field(default=EstadoCobro.PENDIENTE, description="Estado actual del cobro")
    mensaje_estado: str = Field(default="", description="Mensaje de estado (opcional)")
    fecha_intento: datetime = Field(default_factory=datetime.utcnow, description="Fecha del intento de cobro")
    fecha_aprobacion: datetime | None = Field(default=None, description="Fecha de aprobación")
    fecha_rechazo: datetime | None = Field(default=None, description="Fecha de rechazo")
    motivo_rechazo: str | None = Field(default=None, description="Motivo del rechazo (si aplica)")
    reembolsado: bool = Field(default=False, description="Indica si el cobro ha sido reembolsado")
    fecha_reembolso: datetime | None = Field(default=None, description="Fecha del reembolso (si aplica)")
    metadata: dict = Field(default_factory=dict, description="Metadatos adicionales")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "cobros"
        use_state_management = True

    def __str__(self) -> str:
        return f"Cobro {self.id} - {self.estado} - ${self.monto} {self.moneda}"

    class Config:
        json_schema_extra = {
            "example": {
                "cliente_id": "550e8400-e29b-41d4-a716-446655440000",
                "tarjeta_id": "660e8400-e29b-41d4-a716-446655440001",
                "monto": 100.50,
                "moneda": "MXN",
                "descripcion": "Compra en tienda en línea",
                "estado": "pendiente",
                "mensaje_estado": "Esperando procesamiento",
                "fecha_intento": "2023-01-01T12:00:00",
                "metadata": {},
                "reembolsado": False
            }
        }