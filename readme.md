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

## Run Day 3 Script

```bash
python Day3\scraper.py
```

## What the Day 3 Script Does

- visits the main books page
- extracts book details from each product card
- follows pagination through the next page link
- converts prices into float values
- converts rating words like One, Two, Three into numbers
- calculates total books and average price

## Notes

This is a learning project. Use scraping responsibly and respect the website's rules.
