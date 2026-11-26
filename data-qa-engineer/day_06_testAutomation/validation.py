    
    
def validate_price(price):

    if price is None:
        return False

    if not isinstance(price, (int, float)):
        return False

    if isinstance(price, bool):
        return False

    return price > 0