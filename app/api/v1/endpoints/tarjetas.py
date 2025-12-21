# app/api/v1/endpoints/tarjetas.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.crud import crud_tarjeta, crud_cliente
from app.models.tarjeta import Tarjeta as TarjetaModel
from app.models.cliente import Cliente
from app.schemas.tarjeta import Tarjeta, TarjetaCreate
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=Tarjeta, status_code=status.HTTP_201_CREATED)
async def create_tarjeta(
    tarjeta_in: TarjetaCreate,
    current_user = Depends(get_current_user)
):
    """
    Create a new tarjeta for a cliente.
    """
    # Verify cliente exists
    cliente = await Cliente.find_one({"cliente_id": str(tarjeta_in.cliente_id)})
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    
    # Extract last4 and create masked PAN
    pan_clean = ''.join(filter(str.isdigit, tarjeta_in.pan))
    last4 = pan_clean[-4:]
    bin = pan_clean[:6]
    pan_masked = "*" * (len(pan_clean) - 4) + last4
    
    # Check if last4 already exists for this cliente
    existing_tarjeta = await TarjetaModel.find_one({
        "cliente_id": str(tarjeta_in.cliente_id),
        "last4": last4
    })
    
    if existing_tarjeta:
        raise HTTPException(
            status_code=400,
            detail="A tarjeta with these last 4 digits already exists for this cliente"
        )
    
    # Create the tarjeta with masked PAN
    tarjeta_data = {
        "cliente_id": str(tarjeta_in.cliente_id),
        "pan_masked": pan_masked,
        "last4": last4,
        "bin": bin,
        "descripcion": tarjeta_in.descripcion
    }
    
    return await crud_tarjeta.tarjeta.create(obj_in=tarjeta_data)