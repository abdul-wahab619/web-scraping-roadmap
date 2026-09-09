# Web Scraping Roadmap

A simple learning roadmap for practicing Python web scraping step by step.

## Progress

### Day 1
- Basics of web scraping
- HTML structure and page inspection
- HTTP requests and responses
- Understanding tags, classes, and selectors
- Responsible scraping practices

### Day 2
- Requesting a real website
- Parsing HTML with BeautifulSoup
- Extracting product information
- Collecting title, price, rating, and URL
- Storing data in Python lists and dictionaries

### Day 3
- Scraping multiple pages using pagination
- Following the "Next" button to continue scraping
- Cleaning and converting price values to numbers
- Mapping rating text to numeric values
- Calculating totals like total books and average price

### Day 4
- Saving scraped book data as JSON and CSV files
- Loading saved data from JSON
- Calculating total and average prices
- Finding the most expensive and most affordable books
- Calculating the average book rating

### Day 5
- Using a persistent `requests.Session`
- Setting a custom User-Agent header
- Handling request failures with retries and exponential backoff
- Scraping book detail pages for descriptions and product information
- Saving the expanded data to JSON and CSV files
- Limiting the practice run to two listing pages

### Day 6
- Inspecting network requests with browser developer tools
- Distinguishing static HTML data from API responses
- Sending GET requests to public REST APIs
- Using query parameters such as `limit`, `skip`, `_page`, and `_limit`
- Reading JSON responses and extracting product and post data
- Combining paginated API responses into one list

## Project Structure

```text
web-scraping-roadmap/
├── Day1/
│   └── Web-Scraping-Practices.docx
├── Day2/
│   ├── scraper.py
│   └── scraper1.py
├── Day3/
│   └── scraper.py
├── Day4/
│   ├── analyze.py
│   ├── books.csv
│   ├── books.json
│   └── scraper.py
├── Day5/
│   ├── books.csv
│   ├── books.json
│   └── scraper.py
├── Day6/
│   ├── api-test.py
│   ├── api.py
│   └── exercise.txt
├── readme.md
└── .gitignore
```

## Tools Used

- Python
- requests
- BeautifulSoup
- urllib.parse
- Public REST APIs

## Example Source

https://books.toscrape.com/

## Run Day 5 Script

```bash
python Day5\scraper.py
```

## What the Day 5 Script Does

- create a reusable HTTP session with a custom User-Agent
- retry temporary failures such as HTTP 429 and 5xx responses
- scrape two listing pages and follow pagination
- visit each book's detail page
- extract descriptions, tax values, availability, UPC, and product type
- convert prices and ratings into numeric values
- save the expanded data to `Day5/books.json` and `Day5/books.csv`
- print the total books, first and last books, and average price

## Run Day 6 Scripts

```bash
python Day6\api.py
python Day6\api-test.py
```

## What the Day 6 Scripts Do

- request products from `https://dummyjson.com/products` with pagination parameters
- display the response status, final URL, total products, and returned products
- request ten pages of posts from JSONPlaceholder
- combine the posts from each successful page into one list
- print the total number of posts and the first and last posts
- practice checking response status codes and parsing JSON data

## Notes

This is a learning project. Use scraping responsibly and respect the website's rules.
