from playwright.sync_api import sync_playwright, TimeoutError, Error
from urllib.parse import urljoin
import json
import csv

rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def extract_books(page):

    books = page.locator("article.product_pod")

    books.first.wait_for(state="visible")

    results = []

    for i in range(books.count()):

        book = books.nth(i)

        title_element = book.locator("h3 a")
        price_element = book.locator("p.price_color")
        rating_element = book.locator("p.star-rating")

        if (
            title_element.count() == 0
            or price_element.count() == 0
            or rating_element.count() == 0
        ):
            continue

        title = title_element.get_attribute("title")

        price = float(price_element.inner_text().replace("£", "").strip())

        rating_class = rating_element.get_attribute("class")
        rating_name = rating_class.split()[-1]

        rating = rating_map.get(rating_name)

        product_url = urljoin(page.url, title_element.get_attribute("href"))

        results.append(
            {"title": title, "price": price, "rating": rating, "url": product_url}
        )

    return results


all_books = []

max_pages = 3


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    try:

        page.goto("https://books.toscrape.com/", timeout=30000)

    except TimeoutError:
        print("Page loading timed out.")

    except Error as error:
        print("Navigation failed:", error)

    else:

        page_count = 0

        while page_count < max_pages:

            page_count += 1

            books = extract_books(page)

            all_books.extend(books)

            print(f"Page {page_count}: " f"{len(books)} books collected.")

            if page_count >= max_pages:
                break

            next_button = page.locator("li.next a")

            if next_button.count() == 0:
                print("No next page found.")
                break

            try:

                next_button.click()

                page.wait_for_load_state("domcontentloaded", timeout=30000)

            except TimeoutError:
                print("Page loading timed out.")
                break

            except Error as error:
                print("Navigation failed:", error)
                break

    print("Total books collected:", len(all_books))

    browser.close()


with open("books_playwright.json", "w", encoding="utf-8") as file:

    json.dump(all_books, file, indent=4, ensure_ascii=False)

print("Data saved to books_playwright.json")


with open("books_playwright.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(file, fieldnames=["title", "price", "rating", "url"])

    writer.writeheader()
    writer.writerows(all_books)

print("Data saved to books_playwright.csv")

# Average price calculation
if all_books:
    total_price = sum(book["price"] for book in all_books)
    average_price = total_price / len(all_books)
    print("Average price of books:", round(average_price, 2))
