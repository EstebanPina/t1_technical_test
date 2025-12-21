from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from app.crud import crud_cobro, crud_cliente, crud_tarjeta
from app.models.cobro import Cobro, EstadoCobro
from app.schemas.cobro import Cobro as CobroSchema, CobroCreate, CobroUpdate
from app.api.deps import get_current_user

router = APIRouter()

# Reglas de aprobación/rechazo
def evaluar_reglas_cobro(monto: float, tarjeta_id: UUID):
    """
    Evalúa las reglas de negocio para aprobar o rechazar un cobro.
    Reglas de ejemplo:
    - Rechazar si el monto es mayor a 10,000
    - Aprobar si los últimos 4 dígitos son pares
    - Rechazar si el BIN es 400000
    """
    tarjeta = crud_tarjeta.tarjeta.get(tarjeta_id)
    if not tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    
    if monto > 10000:
        return False, "Monto excede el límite permitido"
    
    if tarjeta.last4.isdigit() and int(tarjeta.last4) % 2 != 0:
        return False, "Tarjeta no cumple con los requisitos"
    
    if tarjeta.bin == "400000":
        return False, "Tarjeta no soportada"
    
    return True, "Cobro aprobado"

@router.post("/", response_model=CobroSchema, status_code=status.HTTP_201_CREATED)
async def crear_cobro(
    cobro_in: CobroCreate,
    current_user = Depends(get_current_user)
):
    """
    Crea un nuevo cobro simulado.
    """
    # Verificar que exista el cliente
    cliente = await crud_cliente.cliente.get(cobro_in.cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Verificar que exista la tarjeta
    tarjeta = await crud_tarjeta.tarjeta.get(cobro_in.tarjeta_id)
    if not tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    
    # Verificar que la tarjeta pertenezca al cliente
    if str(tarjeta.cliente_id) != str(cobro_in.cliente_id):
        raise HTTPException(
            status_code=400,
            detail="La tarjeta no pertenece al cliente especificado"
        )
    
    # Evaluar reglas de negocio
    aprobado, mensaje = evaluar_reglas_cobro(cobro_in.monto, cobro_in.tarjeta_id)
    
    # Crear el cobro
    cobro_data = cobro_in.dict()
    cobro_data.update({
        "estado": EstadoCobro.APROBADO if aprobado else EstadoCobro.RECHAZADO,
        "mensaje_estado": mensaje,
        "fecha_intento": datetime.utcnow(),
        "reembolsado": False
    })
    
    cobro = await crud_cobro.cobro.create(obj_in=cobro_data)
    return cobro

@router.get("/{cobro_id}", response_model=CobroSchema)
async def obtener_cobro(
    cobro_id: UUID,
    current_user = Depends(get_current_user)
):
    """
    Obtiene un cobro por su ID.
    """
    cobro = await crud_cobro.cobro.get(cobro_id)
    if not cobro:
        raise HTTPException(status_code=404, detail="Cobro no encontrado")
    return cobro

@router.get("/cliente/{cliente_id}", response_model=List[CobroSchema])
async def obtener_cobros_por_cliente(
    cliente_id: UUID,
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_user)
):
    """
    Obtiene el historial de cobros de un cliente.
    """
    # Verificar que exista el cliente
    cliente = await crud_cliente.cliente.get(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    cobros = await crud_cobro.cobro.get_by_cliente(
        cliente_id=cliente_id,
        skip=skip,
        limit=limit
    )
    return cobros

@router.post("/{cobro_id}/reembolso", response_model=CobroSchema)
async def reembolsar_cobro(
    cobro_id: UUID,
    current_user = Depends(get_current_user)
):
    """
    Realiza el reembolso de un cobro previamente aprobado.
    """
    cobro = await crud_cobro.cobro.get(cobro_id)
    if not cobro:
        raise HTTPException(status_code=404, detail="Cobro no encontrado")
    
    if cobro.estado != EstadoCobro.APROBADO:
        raise HTTPException(
            status_code=400,
            detail="Solo se pueden reembolsar cobros aprobados"
        )
    
    if cobro.reembolsado:
        raise HTTPException(
            status_code=400,
            detail="El cobro ya ha sido reembolsado"
        )
    
    # Actualizar el cobro como reembolsado
    cobro_actualizado = await crud_cobro.cobro.update(
        db_obj=cobro,
        obj_in={
            "reembolsado": True,
            "fecha_reembolso": datetime.utcnow()
        }
    )
    
    return cobro_actualizado

# Implementación del algoritmo de Luhn
def validar_luhn(numero_tarjeta: str) -> bool:
    """
    Valida un número de tarjeta usando el algoritmo de Luhn.
    """
    try:
        digits = [int(d) for d in str(numero_tarjeta)]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(divmod(d * 2, 10))
        return checksum % 10 == 0
    except (ValueError, IndexError):
        return False

def generar_numero_valido(bin: str, length: int = 16) -> str:
    """
    Genera un número de tarjeta válido usando el algoritmo de Luhn.
    """
    import random
    
    # Asegurar que el BIN sea válido
    if not bin.isdigit() or len(bin) < 6:
        raise ValueError("BIN debe tener al menos 6 dígitos")
    
    # Generar el número de tarjeta
    numero = bin
    while len(numero) < length - 1:
        numero += str(random.randint(0, 9))
    
    # Calcular el dígito de verificación
    digits = [int(d) for d in numero]
    for i in range(len(digits)-1, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    
    checksum = sum(digits) % 10
    if checksum > 0:
        check_digit = 10 - checksum
    else:
        check_digit = 0
    
    return numero + str(check_digit)

# Ejemplos de tarjetas de prueba
TARJETAS_PRUEBA = [
    # Aprobada - Número par, BIN válido, monto bajo
    {
        "numero": "4111111111111111",
        "last4": "1111",
        "bin": "411111",
        "regla": "Siempre aprobada (número par, BIN válido)"
    },
    # Rechazada - Número impar
    {
        "numero": "4111111111111112",
        "last4": "1112",
        "bin": "411111",
        "regla": "Siempre rechazada (número impar)"
    },
    # Rechazada - BIN no permitido
    {
        "numero": "4000001111111111",
        "last4": "1111",
        "bin": "400000",
        "regla": "Siempre rechazada (BIN no permitido)"
    }
]

# Endpoint para generar tarjetas de prueba
@router.post("/tarjetas-prueba/generar", status_code=status.HTTP_201_CREATED)
async def generar_tarjeta_prueba(
    bin: str = "411111",
    last4: str = None,
    current_user = Depends(get_current_user)
):
    """
    Genera una tarjeta de prueba válida.
    """
    try:
        if last4:
            # Generar un número que termine con los últimos 4 dígitos especificados
            numero = generar_numero_valido(bin)
            numero = numero[:-4] + last4[-4:]
            if not validar_luhn(numero):
                raise HTTPException(
                    status_code=400,
                    detail="No se pudo generar una tarjeta válida con los parámetros dados"
                )
        else:
            numero = generar_numero_valido(bin)
        
        return {
            "numero": numero,
            "last4": numero[-4:],
            "bin": numero[:6],
            "valida": validar_luhn(numero)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))