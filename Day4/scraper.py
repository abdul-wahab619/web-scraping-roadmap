import requests
import json
import csv

from bs4 import BeautifulSoup
from urllib.parse import urljoin

rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def scrape_page(url):

    print("Scraping:", url)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

    except requests.RequestException as error:
        print("Request failed:", error)
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

        product_url = urljoin(
            url,
            title_element.get("href")
        )

        book_data = {
            "title": title,
            "price": price,
            "rating": rating,
            "url": product_url
        }

        books.append(book_data)

    next_button = soup.select_one("li.next a")

    if next_button:
        next_url = urljoin(
            url,
            next_button.get("href")
        )
    else:
        next_url = None

    return books, next_url


start_url = "https://books.toscrape.com/"

all_books = []

current_url = start_url

while current_url:

    books, next_url = scrape_page(current_url)

    all_books.extend(books)

    current_url = next_url


print(f"\nTotal books: {len(all_books)}")


# Save JSON

with open("books.json", "w", encoding="utf-8") as file:
    json.dump(
        all_books,
        file,
        indent=4,
        ensure_ascii=False
    )


# Save CSV

with open(
    "books.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=["title", "price", "rating", "url"]
    )

    writer.writeheader()
    writer.writerows(all_books)


print("Saved books.json")
print("Saved books.csv")
