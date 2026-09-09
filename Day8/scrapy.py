import requests

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0", "Accept": "application/json"})

response = session.get(
    "https://httpbin.org/cookies/set", params={"course": "web_scraping"}
)
response = session.get("https://httpbin.org/cookies")

print("Session headers:", session.headers)
print("Session cookies:", session.cookies.get_dict())
print("Server sees:", response.json())
