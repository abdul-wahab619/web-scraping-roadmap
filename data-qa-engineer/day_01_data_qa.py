products = [
    {"id": 1, "name": "Laptop", "price": 1200, "rating": 4.5},
    {"id": 2, "name": "Phone", "price": 800, "rating": 4.2},
    {"id": 3, "name": None, "price": 500, "rating": 3.9},
    {"id": 4, "name": "Tablet", "price": -100, "rating": 4.1},
    {"id": 5, "name": "Monitor", "price": 300, "rating": 6.5},
    {"id": 6, "name": "Keyboard", "price": None, "rating": None},
    {"id": 7, "name": "Mouse", "price": "50", "rating": 4.0},
]


def validate_product(product):

    errors = []

    # Check product name
    if not product.get("name"):
        errors.append("Missing product name")

    # Check price
    price = product.get("price")

    if price is None:
        errors.append("Missing price")
    elif not isinstance(price, (int, float)) or isinstance(price, bool):
        errors.append("Price must be numeric")
    elif price <= 0:
        errors.append("Price must be positive")

    # Check rating
    rating = product.get("rating")

    if rating is None:
        errors.append("Missing rating")
    elif not isinstance(rating, (int, float)) or isinstance(rating, bool):
        errors.append("Rating must be numeric")
    elif not 0 <= rating <= 5:
        errors.append("Rating must be between 0 and 5")

    return errors


print("========== DATA QA REPORT ==========")
print("\n")

print("Total products:", len(products))
print(
    "Passed records:", sum(1 for product in products if not validate_product(product))
)
print("Failed records:", sum(1 for product in products if validate_product(product)))

print("\n")

for product in products:

    errors = validate_product(product)

    if errors:
        for index, error in enumerate(errors):
            print(f"Record {product['id']}:")
            print(f"- {error}\n")
    else:
        print(f"Record {product['id']} PASSED\n")

print("========== END OF REPORT ==========")