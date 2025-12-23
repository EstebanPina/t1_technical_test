"""
Módulo de utilidades para validación y generación de números de tarjeta.
Incluye implementación del algoritmo de Luhn.
"""
import random
from typing import List

def luhn_checksum(card_number: str) -> int:
    """
    Calcula el dígito de verificación de Luhn para un número de tarjeta.
    
    Args:
        card_number: Número de tarjeta como string.
        
    Returns:
        int: 0 si el número es válido según Luhn, otro valor en caso contrario.
    """
    digits = [int(d) for d in str(card_number)]
    odd_digits = digits[-1::-2]  # Dígitos en posiciones impares (empezando desde el final)
    even_digits = digits[-2::-2]  # Dígitos en posiciones pares
    
    total = sum(odd_digits)
    
    # Para los dígitos en posiciones pares, multiplicar por 2 y sumar los dígitos
    for d in even_digits:
        total += sum(divmod(d * 2, 10))
    
    return total % 10

def is_valid_card(card_number: str) -> bool:
    """
    Verifica si un número de tarjeta es válido usando el algoritmo de Luhn.
    
    Args:
        card_number: Número de tarjeta a validar.
        
    Returns:
        bool: True si el número es válido, False en caso contrario.
    """
    return luhn_checksum(card_number) == 0

def generate_card_number(bin: str, length: int = 16) -> str:
    """
    Genera un número de tarjeta válido que comienza con el BIN especificado.
    
    Args:
        bin: BIN (Bank Identification Number) como string.
        length: Longitud total del número de tarjeta (por defecto 16).
        
    Returns:
        str: Número de tarjeta válido.
        
    Raises:
        ValueError: Si el BIN no es numérico o es más largo que la longitud deseada.
    """
    if not bin.isdigit():
        raise ValueError("El BIN debe contener solo dígitos")
    
    # Generar los dígitos aleatorios necesarios (excepto el último)
    random_length = length - len(bin) - 1
    if random_length < 0:
        raise ValueError("El BIN es más largo que la longitud deseada de la tarjeta")
    
    # Generar dígitos aleatorios
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(random_length)])
    
    # Calcular el dígito de verificación
    base_number = bin + random_digits
    checksum = luhn_checksum(base_number + '0')
    check_digit = (10 - checksum) % 10
    
    return base_number + str(check_digit)

def generate_card_numbers(bin: str, count: int = 1, length: int = 16) -> List[str]:
    """
    Genera múltiples números de tarjeta válidos.
    
    Args:
        bin: BIN (Bank Identification Number) como string.
        count: Número de tarjetas a generar.
        length: Longitud de cada tarjeta.
        
    Returns:
        List[str]: Lista de números de tarjeta válidos.
    """
    return [generate_card_number(bin, length) for _ in range(count)]
