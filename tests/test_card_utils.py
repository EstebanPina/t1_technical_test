# tests/test_card_utils.py
import pytest
from app.utils.card_utils import (
    luhn_checksum,
    is_valid_card,
    generate_card_number,
    generate_card_numbers
)

def test_luhn_checksum():
    # Test valid card numbers
    assert luhn_checksum("4111111111111111") == 0
    assert luhn_checksum("5555555555554444") == 0
    assert luhn_checksum("4012888888881881") == 0
    
    # Test invalid card numbers
    assert luhn_checksum("4111111111111112") != 0
    assert luhn_checksum("5555555555554445") != 0

def test_is_valid_card():
    # Test valid card numbers
    assert is_valid_card("4111111111111111") is True
    assert is_valid_card("5555555555554444") is True
    assert is_valid_card("4012888888881881") is True
    
    # Test invalid card numbers
    assert is_valid_card("4111111111111112") is False
    assert is_valid_card("1234567812345678") is False
    assert is_valid_card("") is False  # Empty string should be invalid
    assert is_valid_card("abc") is False
    assert is_valid_card("123") is False  # Too short
    assert is_valid_card("12345678901234567890") is False  # Too long

def test_generate_card_number():
    # Test with different BINs and lengths
    card1 = generate_card_number("411111", 16)
    assert len(card1) == 16
    assert card1.startswith("411111")
    assert is_valid_card(card1)
    
    card2 = generate_card_number("555555", 16)
    assert len(card2) == 16
    assert card2.startswith("555555")
    assert is_valid_card(card2)
    
    # Test with custom length
    card3 = generate_card_number("34", 15)  # AMEX
    assert len(card3) == 15
    assert is_valid_card(card3)

def test_generate_card_numbers():
    # Test generating multiple cards
    cards = generate_card_numbers("411111", count=3, length=16)
    assert len(cards) == 3
    for card in cards:
        assert len(card) == 16
        assert card.startswith("411111")
        assert is_valid_card(card)
    
    # Test with different count
    cards = generate_card_numbers("555555", count=5, length=16)
    assert len(cards) == 5
    for card in cards:
        assert len(card) == 16
        assert card.startswith("555555")
        assert is_valid_card(card)

def test_invalid_bin():
    # Test with non-numeric BIN
    with pytest.raises(ValueError):
        generate_card_number("abc", 16)
    
    # Test with empty BIN
    with pytest.raises(ValueError):
        generate_card_number("", 16)

def test_card_number_length():
    # Test with invalid length
    with pytest.raises(ValueError):
        generate_card_number("411111", 10)  # Too short
    
    with pytest.raises(ValueError):
        generate_card_number("411111", 20)  # Too long