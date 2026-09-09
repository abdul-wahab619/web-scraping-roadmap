from playwright.sync_api import sync_playwright, TimeoutError


def scrape_infinite_scroll(page, selector, max_scrolls=10):

    paragraphs = page.locator(selector)

    # Initial count
    current_count = paragraphs.count()

    print("Initial paragraphs:", current_count)

    scroll_count = 0

    processed_count = 0
    all_paragraphs = []

    # Extract initial paragraphs
    for i in range(processed_count, current_count):
        text = paragraphs.nth(i).inner_text().strip()
        all_paragraphs.append(text)

    processed_count = current_count

    while scroll_count < max_scrolls:

        scroll_count += 1

        # Scroll the last paragraph into view
        paragraphs.last.scroll_into_view_if_needed()

        # Wait for new content
        try:
            page.wait_for_function(
                """([selector, processed_count]) => {
                    return document.querySelectorAll(selector).length > processed_count;
                }""",
                arg=[selector, processed_count],
                timeout=5000,
            )

        except TimeoutError:
            print("No new content loading. " f"Stopping at scroll {scroll_count}")
            break

        # Count paragraphs again
        current_count = paragraphs.count()

        print("Scroll", scroll_count, ":", current_count, "paragraphs")

        # Stop if no new paragraphs were loaded
        if current_count == processed_count:
            break

        # Extract only newly loaded paragraphs
        for i in range(processed_count, current_count):
            text = paragraphs.nth(i).inner_text().strip()
            all_paragraphs.append(text)

        # Update processed count
        processed_count = current_count

    return all_paragraphs, scroll_count


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://the-internet.herokuapp.com/infinite_scroll")

    paragraphs, scroll_count = scrape_infinite_scroll(
        page, ".jscroll-added", max_scrolls=10
    )

    print("Collected:", len(paragraphs))
    print("Scrolls performed:", scroll_count)

    print("\nFirst 3 paragraphs:")

    for paragraph in paragraphs[:3]:
        print(paragraph)
        print()

    browser.close()
