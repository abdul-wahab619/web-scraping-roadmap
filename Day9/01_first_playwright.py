from playwright.sync_api import sync_playwright

rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://books.toscrape.com/")

    print("Page title:", page.title())

    books = page.locator("article.product_pod")

    print("Number of books found:", books.count())

    book = books.first

    title = book.locator("h3 a").get_attribute("title")
    price = book.locator("p.price_color").inner_text()

    rating_element = book.locator("p.star-rating")
    classes = rating_element.get_attribute("class")
    rating = classes.split()[-1]
    rating = rating_map.get(rating, 0)

    print("Title:", title)
    print("Price:", price)
    print("Rating:", rating)

    browser.close()
