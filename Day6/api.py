import requests

url = "https://dummyjson.com/products"

params = {"limit": 10, "skip": 10}

response = requests.get(url, params=params)

data = response.json()
products = data["products"]

print(response.status_code)
print(response.url)
    
print("Total products:", data["total"])
print("Products returned:", len(products))
print("First product:", products[0])
print("Last product:", products[-1])
