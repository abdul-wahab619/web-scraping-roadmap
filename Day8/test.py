import requests

url = "https://httpbin.org/anything"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://example.com/products",
}

params = {"page": 2, "limit": 20}

cookies = {"session_id": "demo-session"}

response = requests.get(url, headers=headers, params=params, cookies=cookies)

response.raise_for_status()

data = response.json()

# print the required values
print("Status:", response.status_code)
print("URL:", response.url)
print("User-Agent:", data["headers"].get("User-Agent"))
print("Accept:", data["headers"].get("Accept"))
print("Referer:", data["headers"].get("Referer"))
print("Query Parameters:", data["args"])
print("Cookies:", data["headers"].get("Cookie"))
