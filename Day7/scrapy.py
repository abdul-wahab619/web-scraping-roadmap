import requests
import time
import json
import csv

url = "https://dummyjson.com/products"

retryable_status_codes = {429, 500, 502, 503, 504}


def get_page(url, params, retries=3):
    for attempt in range(retries):
        time.sleep(0.5)

        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code in retryable_status_codes:
                print(f"Retryable error: " f"{response.status_code}")

                if attempt < retries - 1:
                    wait_time = 2**attempt
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)

                continue

            response.raise_for_status()
            return response

        except requests.RequestException as error:
            print(f"Request failed " f"(attempt {attempt + 1}/{retries}):", error)

            if attempt < retries - 1:
                wait_time = 2**attempt
                time.sleep(wait_time)

    return None


def scrape_products(limit=20):
    skip = 0
    all_products = []

    max_pages = 100
    page_count = 0

    while True:

        params = {"limit": limit, "skip": skip}

        response = get_page(url, params=params)

        if response is None:
            print("Failed to fetch page.")
            break
        print("Scraping products page:", response.url)

        data = response.json()

        products = data.get("products")

        if not isinstance(products, list):
            print("Invalid products data. Stopping.")
            break

        if not products:
            print("No products returned. Stopping.")
            break

        all_products.extend(products)

        print(f"Fetched {len(products)} products | " f"skip={skip}")

        skip += limit

        if len(all_products) >= data["total"]:
            break

        page_count += 1

        if page_count >= max_pages:
            print("Reached maximum number of pages. Stopping.")
            break

    return all_products


products = scrape_products(limit=20)

print("Total products collected:", len(products))
print("First product:", products[0])
print("Last product:", products[-1])

with open("products.json", "w", encoding="utf-8") as file:
    json.dump(products, file, indent=4, ensure_ascii=False)

with open("products.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = products[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(products)


print("Saved products.json")
print("Saved products.csv")
