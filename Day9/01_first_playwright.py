from playwright.sync_api import sync_playwright

rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://books.toscrape.com/")

    print("Page title:", page.title())

    books = page.locator("article.product_pod")

    books.first.wait_for(state="visible")

    print("Number of books found:", books.count())

    first_book = books.first

    title = first_book.locator("h3 a").get_attribute("title")
    price = first_book.locator("p.price_color").inner_text()

    print("Title:", title)
    print("Price:", price)

    browser.close()
