from bs4 import BeautifulSoup  
from lxml import html          

# ---------- Task 1: read sample.html ----------
with open("sample.html", "r", encoding="utf-8") as file:
    html_text = file.read()

# ---------- Task 2: parse it with BeautifulSoup ----------
soup = BeautifulSoup(html_text, "html.parser")

# ---------- Task 3: extract all .product-card elements ----------
cards = soup.select(".product-card")
print(f"Found {len(cards)} product cards\n")


# Helper: return the text of the first match, or None if nothing matches
def get_text(card, selector):
    element = card.select_one(selector)
    return element.get_text(strip=True) if element else None


css_results = []

for card in cards:
    # ---------- Task 4: title using CSS ----------
    title = get_text(card, ".product-title")

    # ---------- Task 5: price using CSS ----------
    price = get_text(card, ".price")

    # ---------- Task 6: availability ----------
    availability = get_text(card, ".availability")

    # ---------- Task 7: product link ----------
    link_tag = card.select_one("a[href]")
    link = link_tag["href"] if link_tag else None

    css_results.append({
        "id": card.get("id"),
        "title": title,
        "price": price,
        "availability": availability,
        "link": link,
    })

# ---------- Task 8: repeat title and price using XPath ----------
tree = html.fromstring(html_text)
xpath_cards = tree.xpath('//div[@class="product-card"]')

xpath_results = []

for card in xpath_cards:
    title_list = card.xpath('.//h2[@class="product-title"]/text()')
    price_list = card.xpath('.//p[@class="price"]/text()')

    xpath_results.append({
        "id": card.get("id"),
        "title": title_list[0].strip() if title_list else None,
        "price": price_list[0].strip() if price_list else None,
    })

# ---------- Task 9: detect missing title, price, or link ----------
problems = []

for item in css_results:
    missing = []
    if item["title"] is None:
        missing.append("title")
    if item["price"] is None:
        missing.append("price")
    if item["link"] is None:
        missing.append("link")

    if missing:
        problems.append((item["id"], missing))

# ---------- Task 10: extraction QA report ----------
print("===== EXTRACTION QA REPORT =====")
print(f"Total cards: {len(cards)}")
print(f"Complete cards: {len(cards) - len(problems)}")
print(f"Cards with missing data: {len(problems)}\n")

print("CSS results:")
for item in css_results:
    print(f"  {item['id']}: {item['title']} | {item['price']} | "
          f"{item['availability']} | {item['link']}")

print("\nXPath results (title, price):")
for item in xpath_results:
    print(f"  {item['id']}: {item['title']} | {item['price']}")

print("\nMissing data:")
if problems:
    for card_id, missing in problems:
        print(f"  {card_id}: missing {', '.join(missing)}")
else:
    print("  None")

# Check that CSS and XPath agree
print("\nCSS vs XPath match:")
for css_item, xpath_item in zip(css_results, xpath_results):
    same = (css_item["title"] == xpath_item["title"]
            and css_item["price"] == xpath_item["price"])
    print(f"  {css_item['id']}: {'match' if same else 'different'}")