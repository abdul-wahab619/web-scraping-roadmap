# our next mini-task

# Before I give you the full Day 5 implementation, write a small test against one book detail page that:

# Requests the page
# Creates the BeautifulSoup object
# Selects the table
# Loops through tr
# Extracts <th> and <td>
# Creates the details dictionary
# Prints the dictionary

import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

price_keys={
    "Price (incl. tax)", "Price (excl. tax)", "Tax"
}
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def scrape_detail_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    
    except requests.RequestException as error:
        print("Request failed:", error)
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    description_element = soup.select_one("div#product_description + p")
    # print(description_element)

    table = soup.select_one("table.table-striped")

    rows = table.select("tr")

    details = {}

    for row in rows:
        key = row.select_one("th")
        value = row.select_one("td")

        if key and value:
            key = key.get_text(strip=True)
            value = value.get_text(strip=True)

            details[key] = value
            
            if key in price_keys:
                price = value.replace("£", "")
                price = float(price)
                details[key] = price
                
            
    details["description"] = (
        description_element.get_text(strip=True)
        if description_element
        else None
    )

    return details


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

    all_books = soup.select("article.product_pod")[:2]

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
        
        detail_data = scrape_detail_page(product_url)
        
        book_data = {
            "title": title,
            "price": price,
            "rating": rating,
            "url": product_url
        }

        if detail_data:
            book_data.update(detail_data)

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

books, next_url = scrape_page(start_url)

print(f"Total books: {len(books)}")


for book in books:
    print(book)