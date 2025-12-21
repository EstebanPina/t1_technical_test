from typing import List
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.crud import crud_cliente
from app.models.cliente import Cliente
from app.schemas.cliente import Cliente as ClienteSchema, ClienteCreate, ClienteUpdate
from app.api.deps import get_db

router = APIRouter()

@router.get("/", response_model=List[ClienteSchema])
async def read_clientes(skip: int = 0, limit: int = 100):
    """
    Retrieve clientes with pagination.
    """
    clientes = await crud_cliente.cliente.get_multi(skip=skip, limit=limit)
    return clientes

@router.post("/", response_model=ClienteSchema, status_code=201)
async def create_cliente(*, cliente_in: ClienteCreate):
    """
    Create a new cliente.
    """
    # Check if email already exists
    cliente = await crud_cliente.cliente.get_by_email(email=cliente_in.email)
    if cliente:
        raise HTTPException(
            status_code=400,
            detail="The cliente with this email already exists.",
        )
    
    # Check if phone number already exists
    cliente = await crud_cliente.cliente.get_by_telefono(telefono=cliente_in.telefono)
    if cliente:
        raise HTTPException(
            status_code=400,
            detail="The phone number is already registered.",
        )
    
    return await crud_cliente.cliente.create(obj_in=cliente_in)

@router.get("/{cliente_id}", response_model=ClienteSchema)
async def read_cliente(cliente_id: UUID):
    """
    Get a specific cliente by ID.
    """
    cliente = await crud_cliente.cliente.get(id=cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return cliente

@router.put("/{cliente_id}", response_model=ClienteSchema)
async def update_cliente(*, cliente_id: UUID, cliente_in: ClienteUpdate):
    """
    Update a cliente.
    """
    cliente = await crud_cliente.cliente.get(id=cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    
    # Check if email is being updated and if it's already taken
    if cliente_in.email and cliente_in.email != cliente.email:
        existing_cliente = await crud_cliente.cliente.get_by_email(email=cliente_in.email)
        if existing_cliente:
            raise HTTPException(
                status_code=400,
                detail="The email is already registered.",
            )
    
    # Check if phone number is being updated and if it's already taken
    if cliente_in.telefono and cliente_in.telefono != cliente.telefono:
        existing_cliente = await crud_cliente.cliente.get_by_telefono(telefono=cliente_in.telefono)
        if existing_cliente:
            raise HTTPException(
                status_code=400,
                detail="The phone number is already registered.",
            )
    
    return await crud_cliente.cliente.update(db_obj=cliente, obj_in=cliente_in)

@router.delete("/{cliente_id}", status_code=204)
async def delete_cliente(cliente_id: UUID):
    """
    Delete a cliente.
    """
    cliente = await crud_cliente.cliente.remove(id=cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return {"ok": True}
