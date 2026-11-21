import json  # Task 1
import math

# ---------- Task 2 & 3: read the file safely ----------
try:
    with open("products.json", "r", encoding="utf-8") as file:
        data = json.load(file)
except FileNotFoundError:
    print("Error: products.json not found")
    exit()
except json.JSONDecodeError:
    print("Error: invalid JSON format")
    exit()

# ---------- Task 4: get the products list ----------
if not isinstance(data, dict):
    print("Error: JSON root must be an object")
    exit()

products = data.get("products", [])

if not isinstance(products, list):
    print("Error: products must be a list")
    exit()

# ---------- Task 5 & 6: clean the price and convert to float ----------


def normalize_price(price):

    if price is None or isinstance(price, bool):
        return None

    try:
        normalized = float(str(price).replace("$", "").replace(",", "").strip())

        if not math.isfinite(normalized):
            return None

        return normalized

    except (ValueError, TypeError):
        return None


# ---------- Task 7: safely read the nested rating ----------
def get_rating(rating):
    if not isinstance(rating, dict):  # rating is null or missing
        return None

    value = rating.get("value")

    if isinstance(value, (int, float)):
        return value

    if isinstance(value, bool):
        return None

    return None


# ---------- Task 8: validate name, price, rating ----------
def find_issues(name, price, rating):
    issues = []

    if not isinstance(name, str) or not name.strip():
        issues.append("missing name")

    if price is None:
        issues.append("invalid price")
    elif price <= 0:
        issues.append("price must be positive")

    if rating is None:
        issues.append("missing rating")
    elif rating < 0 or rating > 5:
        issues.append("rating out of range")

    return issues


# ---------- Process every product ----------
cleaned_products = []
invalid_count = 0

print("===== QA REPORT =====")

for product in products:
    name = product.get("name")
    price = normalize_price(product.get("price"))
    rating = get_rating(product.get("rating"))
    issues = find_issues(name, price, rating)

    cleaned_products.append(
        {
            "id": product.get("id"),
            "name": name,
            "price": price,
            "rating": rating,
            "is_valid": len(issues) == 0,
            "issues": issues,
        }
    )

    # ---------- Task 9: report problems ----------
    if issues:
        invalid_count += 1
        print(f"Product {product.get('id')}: FAILED")

        for issue in issues:
            print(f"  - {issue}")
    else:
        print(f"Product {product.get('id')}: PASSED")

print("---------------------")
print(f"Total products: {len(products)}")
print(f"Valid: {len(products) - invalid_count}")
print(f"Invalid: {invalid_count}")

# ---------- Task 10: save cleaned data ----------
with open("cleaned_products.json", "w", encoding="utf-8") as file:
    json.dump(cleaned_products, file, indent=4)

print("Saved to cleaned_products.json")
