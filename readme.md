# Web Scraping Roadmap

A practical learning journey designed to help beginners understand how web scraping works step by step using Python. This repository documents the progress of each day, starting from the fundamentals of web pages and HTTP requests to extracting real data from websites.

## Project Goal

The main objective of this roadmap is to build a strong foundation in:

- understanding how websites are structured
- sending HTTP requests and reading responses
- scraping data from HTML using Python
- selecting elements with BeautifulSoup
- handling scraped data in a structured way
- following ethical and responsible scraping practices

---

## Learning Progress by Day

### Day 1: Foundations of Web Scraping

Day 1 focuses on the core concepts before writing any scraper.

#### Topics covered
- What web scraping is and why it is useful
- How websites are built using HTML and CSS
- How browsers and servers communicate through HTTP requests
- Understanding tags, attributes, classes, and selectors
- Exploring the structure of a webpage before extracting data
- Learning safe and responsible scraping practices
- Reviewing best practices and project expectations

#### Day 1 outcome
By the end of Day 1, learners should be able to understand how information is stored in HTML and how to inspect a webpage before writing a script to collect data.

#### Files related to Day 1
- Day1/Web-Scraping-Practices.docx

---

### Day 2: Scraping Data from a Real Website

Day 2 moves from theory into practice by fetching data from a live website and extracting useful information.

#### Topics covered
- sending requests to a website using Python
- parsing HTML content with BeautifulSoup
- selecting a single product from a page
- selecting multiple products from the page
- extracting fields like:
  - title
  - price
  - rating
  - product URL
- storing the extracted results in Python dictionaries and lists

#### Tools used
- Python
- requests
- BeautifulSoup

#### Practice source
The sample project uses the public website: https://books.toscrape.com/

#### Files related to Day 2
- Day2/scraper.py
- Day2/scraper1.py

#### What the scripts do
- scraper.py extracts data from one book item and prints the selected details
- scraper1.py loops through all product items and collects structured book information

Example data extracted includes:
- Title
- Price
- Rating
- URL

---

## Repository Structure

```text
web-scraping-roadmap/
├── Day1/
│   └── Web-Scraping-Practices.docx
├── Day2/
│   ├── scraper.py
│   └── scraper1.py
├── readme.md
└── .gitignore
```

---

## Setup Instructions

1. Clone the repository
2. Open the project in your preferred code editor
3. Create a virtual environment
4. Install the required packages

```bash
python -m venv .venv
.venv\Scripts\activate
pip install requests beautifulsoup4
```

---

## How to Run the Day 2 Scripts

### Run the single-product scraper

```bash
python Day2\scraper.py
```

### Run the multi-product scraper

```bash
python Day2\scraper1.py
```

These scripts fetch the HTML from the target page and print the collected book information in a readable format.

---

## What We Learned So Far

- Web pages can be inspected and understood before scraping
- HTML elements can be targeted through selectors
- BeautifulSoup makes parsing easier and cleaner
- Python dictionaries and lists help preserve structured data
- Real websites often require attention to selectors and content structure

---

## Roadmap Ahead

This repository is expected to grow day by day with more advanced topics such as:

- pagination
- handling errors and timeouts
- saving scraped data to CSV and JSON
- cleaning and validating extracted content
- scraping dynamic websites
- building mini real-world scraping projects

---

## Notes

This project is designed for learning and practice. Always check a website's Terms of Service and use scraping responsibly and ethically. Avoid scraping sites in ways that may overload servers or violate rules.

---

## Summary

This repository is a beginner-friendly web scraping roadmap that documents progress from basic understanding to practical data extraction. Day 1 establishes the foundation, and Day 2 demonstrates how to scrape structured data from a real webpage using Python.

If you are following the roadmap, each new day should build on the previous one and gradually improve your skill set.
