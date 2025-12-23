# tests/test_card_utils.py
import pytest
from app.utils.card_utils import (
    luhn_checksum, 
    is_valid_card, 
    generate_card_number,
    generate_card_numbers
)

def test_luhn_checksum():
    # Números de tarjeta de prueba conocidos
    assert luhn_checksum("4111111111111111") == 0  # Válido
    assert luhn_checksum("4111111111111112") != 0  # Inválido
    assert luhn_checksum("49927398716") == 0  # Otro ejemplo válido

def test_is_valid_card():
    assert is_valid_card("4111111111111111") is True
    assert is_valid_card("4111111111111112") is False
    assert is_valid_card("49927398716") is True

def test_generate_card_number():
    # Probar con diferentes BINs
    test_bins = ["4", "51", "34", "37", "5", "6011"]
    for bin in test_bins:
        card = generate_card_number(bin)
        assert card.startswith(bin)
        assert is_valid_card(card)
    
    # Probar diferentes longitudes
    for length in [13, 16, 19]:
        card = generate_card_number("4", length)
        assert len(card) == length
        assert is_valid_card(card)

def test_generate_card_numbers():
    # Generar múltiples tarjetas
    cards = generate_card_numbers("4", 5)
    assert len(cards) == 5
    assert len(set(cards)) == 5  # Todos deben ser únicos
    
    # Verificar que todas son válidas
    for card in cards:
        assert is_valid_card(card)

def test_invalid_bin():
    with pytest.raises(ValueError):
        generate_card_number("abc")  # BIN no numérico
    
    with pytest.raises(ValueError):
        generate_card_number("12345678901234567")  # BIN más largo que la longitud deseada

def test_card_number_length():
    # Probar que la longitud generada es correcta
    for length in [13, 16, 19]:
        card = generate_card_number("4", length)
        assert len(card) == length