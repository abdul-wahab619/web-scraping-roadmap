from validation import validate_price


def test_valid_price():
    assert validate_price(100) is True


def test_zero_price():
    assert validate_price(0) is False


def test_negative_price():
    
    assert validate_price(-10) is False


def test_missing_price():
    assert validate_price(None) is False


def test_string_price():
    assert validate_price("100") is False


def test_boolean_price():
    assert validate_price(True) is False 
