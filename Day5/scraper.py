import time
import requests
import json
import csv
from urllib.parse import urljoin
from bs4 import BeautifulSoup

price_keys = {"Price (incl. tax)", "Price (excl. tax)", "Tax"}
rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

session = requests.Session()

session.headers.update(
    {"User-Agent": "Mozilla/5.0 (compatible; WebScrapingCourse/1.0)"}
)

retryable_status_codes = {429, 500, 502, 503, 504}


def get_page(url, retries=3):

    for attempt in range(retries):

        time.sleep(0.5)

        try:
            response = session.get(url, timeout=10)

            if response.status_code in retryable_status_codes:

                print(f"Non-retryable HTTP error: {response.status_code}")

                if attempt < retries - 1:
                    wait_time = 2**attempt
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)

                continue

            if response.status_code >= 400:

                print(f"Non-retryable HTTP error: {response.status_code}")

                return None

            return response

        except requests.RequestException as error:

            print(f"Request failed " f"(attempt {attempt + 1}/{retries}): {error}")

            if attempt < retries - 1:
                wait_time = 2**attempt
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

    print("All retry attempts failed.")
    return None


def scrape_detail_page(url):

    print("Scraping detail page:", url)
    response = get_page(url)

    if response is None:
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    description_element = soup.select_one("div#product_description + p")
    # print(description_element)

    table = soup.select_one("table.table-striped")
    details = {}

    if table:
        rows = table.select("tr")

        for row in rows:
            key = row.select_one("th")
            value = row.select_one("td")

            if key and value:
                key = key.get_text(strip=True)
                value = value.get_text(strip=True)

                if key in price_keys:
                    value = float(value.replace("£", ""))

                details[key] = value

    details["description"] = (
        description_element.get_text(strip=True) if description_element else None
    )
    return details


def scrape_page(url):

    print("Scraping:", url)

    response = get_page(url)
    if response is None:
        return [], None
    soup = BeautifulSoup(response.content, "html.parser")

    books = []

    all_books = soup.select("article.product_pod")

    for book in all_books:

        title_element = book.select_one("h3 a")
        price_element = book.select_one("p.price_color")
        rating_element = book.select_one("p.star-rating")

        if not title_element or not price_element or not rating_element:
            continue

        title = title_element.get_text(strip=True)

        price = price_element.get_text(strip=True)
        price = price.replace("£", "")
        price = float(price)

        rating_name = rating_element.get("class")[1]
        rating = rating_map[rating_name]

        product_url = urljoin(url, title_element.get("href"))

        detail_data = scrape_detail_page(product_url)

        book_data = {
            "title": title,
            "price": price,
            "rating": rating,
            "url": product_url,
        }

        if detail_data:
            book_data.update(detail_data)

        books.append(book_data)

    next_button = soup.select_one("li.next a")

    if next_button:
        next_url = urljoin(url, next_button.get("href"))
    else:
        next_url = None

    return books, next_url


start_url = "https://books.toscrape.com/"

current_url = start_url

all_books = []

page_number = 1

while current_url and page_number <= 2:
    print(f"Scraping page {page_number}")
    books, next_url = scrape_page(current_url)

    all_books.extend(books)

    current_url = next_url
    page_number += 1

# print(f"Total books: {len(all_books)}")

with open("books.json", "w", encoding="utf-8") as file:
    json.dump(all_books, file, indent=4, ensure_ascii=False)

# print("Saved data to books.json of length:", len(all_books))

if all_books:

    fieldnames = all_books[0].keys()

    with open("books.csv", "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(all_books)

# print("Saved data to books.csv")

print(f"Total books: {len(all_books)}")

if all_books:

    print("\nFirst book:")
    print(all_books[0])

    print("\nLast book:")
    print(all_books[-1])

    print("\nAverage price:")

    average_price = sum(book["price"] for book in all_books) / len(all_books)

    print(f"£{average_price:.2f}")
