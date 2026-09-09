import requests

url = "https://jsonplaceholder.typicode.com/posts"

all_posts = []

for page in range(1, 11):
    params = {"_page": page, "_limit": 10}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        all_posts.extend(data)
    else:
        print(f"Failed to fetch page {page}: {response.status_code}")


print("Total posts fetched:", len(all_posts))
print("First Post:", all_posts[0])
print("Last Post:", all_posts[-1])
