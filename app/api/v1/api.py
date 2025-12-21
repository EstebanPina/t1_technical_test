from fastapi import APIRouter
from app.api.v1.endpoints import clientes, tarjetas, cobros

api_router = APIRouter()

# Include routers
api_router.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
api_router.include_router(tarjetas.router, prefix="/tarjetas", tags=["Tarjetas"])
api_router.include_router(cobros.router, prefix="/cobros", tags=["Cobros"])
