import requests
from bs4 import BeautifulSoup

from pprint import pprint


url = "https://books.toscrape.com/"

response = requests.get(url)

print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

all_books = soup.select("article.product_pod")
# print(all_books)
print(f"Found {len(all_books)} books on the page.")

books = []

# convert all books to show in a loop
# print("----------------------------")
for book in all_books:

    title_element = book.select_one("h3 a")
    price_element = book.select_one("p.price_color")
    rating_element = book.select_one("p.star-rating")

    title = title_element.get_text(strip=True)
    price = price_element.get_text(strip=True)
    rating = rating_element.get("class")[1]
    product_url = title_element.get("href")

    # print("Title:", title)
    # print("Price:", price)
    # print("Rating:", rating)
    # print("URL:", product_url)
    # print("----------------------------")

    books_dict = {
        "title": title,
        "price": price,
        "rating": rating,
        "url": product_url
    }

    books.append(books_dict)

# print(books)
pprint(books)

