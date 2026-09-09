from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://the-internet.herokuapp.com/login")

    print("Title:", page.title())

    username = page.locator("#username")
    password = page.locator("#password")

    username.fill("tomsmith")
    password.fill("SuperSecretPassword!")

    page.get_by_role("button", name="Login").click()

    page.wait_for_load_state("domcontentloaded")

    print("URL:", page.url)

    flash_message = page.locator(".flash.success")
    flash_message.wait_for(state="visible")

    print("Flash message:", flash_message.inner_text().strip())

    browser.close()
