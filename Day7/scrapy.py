import requests
import time

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

    while True:
        params = {"limit": limit, "skip": skip}

        response = get_page(url, params=params)

        if response is None:
            print("Failed to fetch page.")
            break
        print("Scraping products page:", response.url)

        data = response.json()
        products = data["products"]
        all_products.extend(products)

        print(f"Fetched {len(products)} products | " f"skip={skip}")

        skip += limit

        if len(all_products) >= data["total"]:
            break

    return all_products


products = scrape_products(limit=20)

print("Total products collected:", len(products))
print("First product:", products[0])
print("Last product:", products[-1])
