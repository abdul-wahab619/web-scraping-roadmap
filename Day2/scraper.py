import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"

response = requests.get(url)

print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

book = soup.select_one("article.product_pod")

# title_element = book.select_one("h3 a")

# print(title_element)

# print(title_element.get("title"))

# print(title_element.attrs.get("title"))

# print(title_element.text)

# title = title_element.get_text(strip=True)

# print(title)

# print(book)

# print(soup)


# price_element = book.select_one("p.price_color")

# price = price_element.get_text(strip=True)

# print(price_element)
# print(price)

# rating_element = book.select_one("p.star-rating")

# print(rating_element.get("class")[1])

# url= title_element.get("href")

# print(url)

# more clean way to get data

title_element = book.select_one("h3 a")
price_element = book.select_one("p.price_color")
rating_element = book.select_one("p.star-rating")

title = title_element.get_text(strip=True)
price = price_element.get_text(strip=True)
rating = rating_element.get("class")[1]
product_url = title_element.get("href")

print("Title:", title)
print("Price:", price)
print("Rating:", rating)
print("URL:", product_url)