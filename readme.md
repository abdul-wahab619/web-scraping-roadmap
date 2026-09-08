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
├── readme.md
└── .gitignore
```

## Tools Used

- Python
- requests
- BeautifulSoup
- urllib.parse

## Example Source

https://books.toscrape.com/

## Run Day 4 Scripts

```bash
python Day4\scraper.py
python Day4\analyze.py
```

## What the Day 4 Scripts Do

- scrape all book pages and extract book details
- follow pagination through the next page link
- convert prices and ratings into numeric values
- save the scraped data to `books.json` and `books.csv`
- load the JSON data for analysis
- calculate total books, average price, and average rating
- find the most expensive and most affordable books

## Notes

This is a learning project. Use scraping responsibly and respect the website's rules.
