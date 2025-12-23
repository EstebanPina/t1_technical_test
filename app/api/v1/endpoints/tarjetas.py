# app/api/v1/endpoints/tarjetas.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from app.crud import crud_tarjeta
from app.models.tarjeta import Tarjeta
from app.schemas.tarjeta import Tarjeta as TarjetaSchema, TarjetaCreate, TarjetaGenerateRequest, TarjetaGenerateResponse
from app.utils.card_utils import is_valid_card, generate_card_numbers
router = APIRouter()

@router.post("/", response_model=TarjetaSchema, status_code=status.HTTP_201_CREATED)
async def create_tarjeta(tarjeta: TarjetaCreate):
    """
    Crea una nueva tarjeta.
    Valida el número de tarjeta usando el algoritmo de Luhn.
    """
    if not is_valid_card(tarjeta.pan):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Número de tarjeta inválido"
        )
    
    # Procesar los datos de la tarjeta
    pan_clean = ''.join(filter(str.isdigit, tarjeta.pan))
    last4 = pan_clean[-4:]
    bin = pan_clean[:6]
    pan_masked = '*' * (len(pan_clean) - 4) + last4
    
    # Crear el diccionario con todos los campos necesarios
    tarjeta_data = {
        "cliente_id": str(tarjeta.cliente_id),  # Convertir UUID a string
        "pan": tarjeta.pan,
        "pan_masked": pan_masked,
        "last4": last4,
        "bin": bin,
        "descripcion": tarjeta.descripcion
    }
    
    db_tarjeta = await crud_tarjeta.tarjeta.create(obj_in=tarjeta_data)
    
    # Convertir el objeto de la base de datos al modelo Pydantic
    return Tarjeta.model_validate(db_tarjeta, from_attributes=True)

@router.get("/", response_model=List[TarjetaSchema])
async def read_tarjetas(skip: int = 0, limit: int = 100):
    """
    Obtiene una lista de tarjetas con paginación.
    """
    return await crud_tarjeta.tarjeta.get_multi(skip=skip, limit=limit)

@router.get("/{tarjeta_id}", response_model=TarjetaSchema)
async def read_tarjeta(tarjeta_id: UUID):
    """
    Obtiene una tarjeta por su ID.
    """
    tarjeta = await crud_tarjeta.tarjeta.get(id=tarjeta_id)
    if not tarjeta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarjeta no encontrada"
        )
    return tarjeta

@router.post(
    "/generate",
    response_model=TarjetaGenerateResponse,
    status_code=status.HTTP_200_OK,
    summary="Genera números de tarjeta válidos",
    description="Genera uno o más números de tarjeta válidos usando el algoritmo de Luhn."
)
async def generate_card_numbers_endpoint(request: TarjetaGenerateRequest):
    """
    Genera números de tarjeta válidos basados en un BIN específico.
    
    - **bin**: Los primeros dígitos de la tarjeta (BIN)
    - **count**: Número de tarjetas a generar (1-50)
    - **length**: Longitud de la tarjeta (13-19 dígitos)
    """
    try:
        cards = generate_card_numbers(
            bin=request.bin,
            count=request.count,
            length=request.length
        )
        return TarjetaGenerateResponse(
            cards=cards,
            bin=request.bin,
            length=request.length
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )