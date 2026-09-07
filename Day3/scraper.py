import requests
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

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    books = []

    all_books = soup.select("article.product_pod")

    for book in all_books:

        title_element = book.select_one("h3 a")
        price_element = book.select_one("p.price_color")
        rating_element = book.select_one("p.star-rating")

        title = title_element.get_text(strip=True)

        price = price_element.get_text(strip=True)
        price = price.replace("£", "")
        price = float(price)

        rating = rating_element.get("class")[1]
        rating = rating_map[rating]

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


print(f"Total books: {len(all_books)}")

total_price = sum(book["price"] for book in all_books)

average_price = total_price / len(all_books)

print("Average price:", average_price)