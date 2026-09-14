# Web Scraping Roadmap

A simple learning roadmap for practicing Python web scraping step by step.

## Progress So Far

- Day 1 -> HTTP + HTML fundamentals       [Done]
- Day 2 -> requests + BeautifulSoup       [Done]
- Day 3 -> Pagination + cleaning           [Done]
- Day 4 -> JSON/CSV + errors               [Done]
- Day 5 -> Detail pages + resilience       [Done]
- Day 6 -> APIs + API discovery            [Done]
- Day 7 -> Robust API scraper              [Done]
- Day 8 -> Headers + cookies + sessions    [Done]
- Day 9 -> Playwright fundamentals         [Done]
- Day 10 -> Advanced Playwright            [Done]
- Day 11 -> Scrapy                          [Done]
- Day 12 -> Scrapy item pipelines          [Done]
- Day 13 -> Data validation + export      [Done]
- Day 14 -> Scrapy callback passing        [Done]
- Day 15 -> Concurrency, Retry & Middleware [Done]
- Day 16 -> Authentication & session handling [Done]
- Day 17 -> Advanced XPath selectors       [Done]
- Day 18 -> Robustness & monitoring        [Done]
- Day 19 -> AutoThrottle & adaptive concurrency [Done]
- Day 20 -> Data quality monitoring        [Done]
- Day 21 -> Scrapy + Playwright integration [Done]
- Day 22 -> Production scraping architecture [Done]
- Day 23 -> PostgreSQL persistence layer   [Done]
- Day 24 -> FastAPI + Scraping Backend     [Done]
- Day 25 -> Background scraping job system [Done]
- Day 26 -> Scheduled crawling system       [Done]
- Day 27 -> Job Listing Aggregator          [Done]

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

### Day 7
- Building a reusable API page-fetching function
- Scraping all products from DummyJSON with `limit` and `skip`
- Retrying temporary failures with exponential backoff
- Handling request timeouts and invalid API responses
- Stopping when all products are collected or the page limit is reached
- Saving API data to JSON and CSV files

### Day 8
- Using a `requests.Session` to preserve request state
- Setting custom headers such as `User-Agent` and `Accept`
- Sending query parameters and cookies with HTTP requests
- Maintaining cookies across multiple requests
- Inspecting the headers, URL, query parameters, and cookies received by a server
- Validating responses with `raise_for_status()`

### Day 9 - Start of Playwright Learning
- Starting browser automation and dynamic web scraping with Playwright
- Launching a Chromium browser and navigating to a web page
- Using locators to find book cards and extract title and price data
- Waiting for page elements and handling navigation timeouts and errors
- Following pagination with the Next button
- Extracting book titles, prices, ratings, and URLs from multiple pages
- Saving Playwright results to JSON and CSV files
- Calculating the average price of collected books

### Day 10 - Advanced Playwright
- Automating login forms with `fill()` and role-based locators
- Waiting for navigation and confirming successful login messages
- Automating infinite-scroll pages
- Scrolling elements into view to load more content
- Waiting for new content with `wait_for_function()`
- Extracting only newly loaded content after each scroll
- Limiting scroll attempts and stopping when no new content appears

### Day 11 - Scrapy
- Creating a Scrapy project with `scrapy startproject`
- Defining a `BookcrawlerItem` for structured data
- Building a spider that scrapes `books.toscrape.com`
- Extracting title, price, rating, and URL with XPath selectors
- Following pagination through the Next link
- Running the spider with `scrapy crawl books`

### Day 12 - Scrapy detail pages and item pipelines
- Following each book's detail page from the listing page
- Extracting book metadata such as UPC, product type, tax, and availability
- Pulling description and review counts from the product detail view
- Cleaning and normalizing scraped values in a Scrapy item pipeline
- Converting price and review fields into numeric types for easier analysis
- Saving the richer dataset to JSON for later inspection and reporting

### Day 13 - Data cleaning, validation, and export
- Passing scraped items through a `BookcrawlerPipeline` for cleaning
- Stripping whitespace and normalizing string fields in the pipeline
- Converting price fields to `float` values for consistent numeric analysis
- Converting review counts to `int` values for downstream filtering
- Validating required fields, price ranges, and review values with `BookValidationPipeline`
- Dropping duplicate books by UPC using a `DuplicateBookPipeline`
- Exporting the final cleaned dataset to JSON for analysis and reporting

### Day 14 - Scrapy callback passing patterns
- Learning how to follow links with `response.follow()`
- Passing metadata between requests with `meta`
- Passing callback arguments explicitly with `cb_kwargs`
- Understanding the flow from listing page to detail URL to authoritative extraction
- Recognizing the architectural pattern of discovery followed by item extraction

### Day 15 - Concurrency, Retry & Middleware
- Learning how Scrapy schedules multiple requests at once
- Understanding concurrency settings and the effect of parallel requests
- Handling temporary failures with retry policies and backoff behavior
- Using downloader and spider middleware to customize request processing
- Adding custom logic between request creation and response handling
- Improving robustness when crawling larger sites or handling flaky connections

### Day 16 - Authentication & session handling
- Managing cookies manually and preserving cookies across requests
- Using basic authentication credentials securely through a `.env` file
- Submitting POST forms with `FormRequest`
- Extracting and sending CSRF tokens with authenticated requests
- Logging in with a session and accessing authenticated pages

### Day 17 - Advanced XPath selectors
- Building XPath selectors for fairly messy real-world pages
- practice `scrapy shell "https://books.toscrape.com/"`

### Day 18 - Robustness & monitoring
- Handling HTTP failures and network failures
- Managing request timeouts and retries
- Using errbacks for failed requests
- Parsing responses safely and detecting missing fields
- Validating scraped data before processing it
- Tracking crawler-level counters
- Using Scrapy signals and extensions
- Reporting crawl statistics and results

### Day 19 - AutoThrottle & adaptive concurrency
- Understanding global concurrency with `CONCURRENT_REQUESTS`
- Limiting per-domain concurrency with `CONCURRENT_REQUESTS_PER_DOMAIN`
- Applying a fixed request delay with `DOWNLOAD_DELAY`
- Using AutoThrottle for dynamic request throttling
- Setting the desired concurrency level with `AUTOTHROTTLE_TARGET_CONCURRENCY`
- Configuring the maximum adaptive delay with `AUTOTHROTTLE_MAX_DELAY`

### Day 20 - Data quality monitoring
- Cleaning scraped values and converting them to the correct types
- Validating required fields and acceptable value ranges
- Detecting and removing duplicate records
- Monitoring data-quality results across the pipeline
- Producing a clean dataset ready for analysis and export

### Day 21 - Scrapy + Playwright integration
- Launching Chromium successfully from a Scrapy spider
- Loading JavaScript-rendered pages with Playwright
- Extracting 10 quotes from dynamic content
- Dropping 0 items during data-quality processing
- Achieving 100% data quality
- Exporting the clean results to `quotes.json`

### Day 22 - Production scraping architecture
- Separating spiders, items, pipelines, middleware, extensions, and settings
- Configuring Playwright as Scrapy's download handler for dynamic pages
- Using the asyncio reactor to support Scrapy and Playwright together
- Centralizing retries, timeouts, concurrency, and AutoThrottle settings
- Layering cleaning, validation, duplicate detection, and quote validation pipelines
- Monitoring crawl events, dropped items, drop reasons, and data-quality scores
- Building a maintainable architecture ready for production scraping workloads

### Day 23 - PostgreSQL persistence layer
- Designing a PostgreSQL schema with constraints
- Integrating Scrapy with PostgreSQL for persistent storage
- Using parameterized SQL statements safely
- Managing database transactions with `commit()`
- Enforcing uniqueness with a `UNIQUE` UPC constraint
- Protecting against duplicates with PostgreSQL UPSERT operations
- Supporting repeated and idempotent crawls
- Validating data before persistence
- Loading database credentials from environment variables

### Day 24: FastAPI + Scraping Backend
- Building a FastAPI backend for the scraped book data
- Connecting FastAPI to the PostgreSQL database
- Creating health-check and book-count endpoints
- Adding paginated book listing with `limit` and `offset`
- Supporting title and description search with `ILIKE`
- Filtering books by rating and price range
- Validating query parameters with FastAPI and Pydantic
- Handling invalid price ranges and missing books with HTTP errors
- Converting database rows into reusable API response objects
- Returning structured book responses with `BooksResponse` and `Book` schemas

### Day 25: Background Scraping Job System
- Running Redis in Docker and connecting with the Redis Python client
- Creating a `scrape_queue` with `LPUSH` and `BRPOP`
- Creating scrape jobs with a unique `job_id` and `queued` status
- Running a continuously listening background worker
- Executing Scrapy separately from the FastAPI application
- Connecting the complete FastAPI -> Worker -> Scrapy -> PostgreSQL workflow
- Tracking job statuses: `queued`, `running`, `completed`, `failed`, and `retrying`
- Recording `created_at`, `started_at`, `completed_at`, and `failed_at` timestamps
- Measuring each attempt with `duration_seconds`
- Storing failure messages in Redis for job inspection

### Day 26: Scheduled Crawling System
- Implementing scheduled crawling
- Configuring runtime schedules through Redis
- Separating the scheduler from the worker
- Coordinating scheduled jobs with a Redis distributed lock
- Applying lock TTLs to prevent stale locks
- Preventing overlapping scheduled runs
- Storing scheduled job metadata
- Tracking `last_run_at` and `next_run_at`
- Recovering from scheduler errors
- Adding structured logging
- Retrying failed jobs automatically in the worker
- Tracking job timestamps and execution duration
- Retrying failed jobs with an attempt counter and `MAX_RETRIES`
- Recalculating `started_at` and `duration_seconds` for every retry attempt

### Day 27: Job Listing Aggregator
- Scraping job listings from YC Jobs with Scrapy
- Extracting structured `JobItem` records
- Applying data-quality checks and processing items through pipelines
- Persisting clean jobs in PostgreSQL
- Enforcing `UNIQUE(source, external_id)` for source-level deduplication
- Using PostgreSQL UPSERT to support repeatable crawls
- Storing 16 clean job listings

```text
YC Jobs
  ↓
Scrapy
  ↓
Extract JobItem
  ↓
Data Quality / Pipelines
  ↓
PostgreSQL
  ↓
UNIQUE(source, external_id)
  ↓
UPSERT
  ↓
16 clean jobs
```

### FastAPI -> Worker -> Scrapy

```text
POST /scrape
      |
    Redis
      |
    Worker
      |
    Scrapy
      |
 PostgreSQL
```

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
├── Day7/
│   ├── products.csv
│   ├── products.json
│   └── scrapy.py
├── Day8/
│   ├── scrapy.py
│   └── test.py
├── Day9/
│   ├── 01_first_playwright.py
│   ├── 02_playwright.py
│   ├── books_playwright.csv
│   └── books_playwright.json
├── Day10/
│   ├── infinite-scrolling.py
│   └── scrap-pwrite.py
├── scrapy_projects/
│   └── bookcrawler/
│       ├── scrapy.cfg
│       └── bookcrawler/
│           ├── __init__.py
│           ├── items.py
│           ├── middlewares.py
│           ├── pipelines.py
│           ├── settings.py
│           └── spiders/
│               ├── __init__.py
│               └── books.py
├── readme.md
└── .gitignore
```

## Tools Used

- Python
- requests
- BeautifulSoup
- urllib.parse
- Public REST APIs
- JSON and CSV file handling
- HTTP sessions, headers, parameters, and cookies
- Playwright browser automation
- Scrapy
- XPath selectors and item pipelines

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

## Run Day 7 Script

```bash
python Day7\scrapy.py
```

## What the Day 7 Script Does

- request products from `https://dummyjson.com/products` in batches of 20
- retry HTTP 429 and 5xx responses with exponential backoff
- handle request exceptions and timeouts
- validate the product list returned by each API response
- stop after collecting all products or reaching the maximum page limit
- save the collected products to `Day7/products.json` and `Day7/products.csv`
- print the total products collected, including the first and last products

## Run Day 8 Scripts

```bash
python Day8\scrapy.py
python Day8\test.py
```

## What the Day 8 Scripts Do

- create a session with custom `User-Agent` and `Accept` headers
- set a course cookie and verify that the session sends it on the next request
- send custom headers, query parameters, and a session cookie to httpbin
- print the status, final URL, received headers, query parameters, and cookies
- practice checking failed HTTP responses with `raise_for_status()`

## Day 9: Start Playwright Learning

Install Playwright and its browser before running the scripts:

```bash
pip install playwright
playwright install chromium
```

## Run Day 9 Scripts

```bash
python Day9\01_first_playwright.py
python Day9\02_playwright.py
```

## What the Day 9 Scripts Do

- open `https://books.toscrape.com/` in a Chromium browser
- display the page title and count the books found on the page
- extract the first book's title and price
- scrape three pages using the Next button
- collect each book's title, price, rating, and URL
- save the collected data to `Day9/books_playwright.json` and `Day9/books_playwright.csv`
- calculate and print the average book price

## Run Day 10 Scripts

```bash
python Day10\scrap-pwrite.py
python Day10\infinite-scrolling.py
```

## What the Day 10 Scripts Do

- open a login page and submit valid username and password credentials
- verify the redirected URL and visible success message
- open an infinite-scroll page and collect dynamically loaded paragraphs
- wait for new content after each scroll
- print the number of collected paragraphs and scrolls performed
- display the first three collected paragraphs

## Day 11 - Scrapy

- Creating a Scrapy project with `scrapy startproject`
- Defining a `BookcrawlerItem` for structured data
- Building a spider that scrapes `books.toscrape.com`
- Extracting title, price, rating, and URL with XPath selectors
- Following pagination through the Next link
- Running the spider with `scrapy crawl books`

## Run Day 11 Script

```bash
cd scrapy_projects\bookcrawler
scrapy crawl books
```

## What the Day 11 Script Does

- crawl the Books to Scrape homepage and all paginated listing pages
- select book cards with XPath and collect item fields
- follow the "next" page link until the end of the catalog
- yield structured data via a Scrapy item object
- print a count of books found on each page during the crawl

## Day 12 - Scrapy detail pages and pipelines

- navigate from each listing item to the product details page
- capture richer fields like UPC, product type, tax, availability, and review count
- clean string values and convert money values to floats in the pipeline
- normalize review totals into integers for downstream analysis
- save the expanded Scrapy output as structured JSON data

## Run Day 12 Script

```bash
cd scrapy_projects\bookcrawler
scrapy crawl books -o books_pipeline.json
```

## What the Day 12 Script Does

- first scrape the book listing pages and collect the core item fields
- then follow each book to its detail page for extra metadata
- pass each item through the pipeline to strip text and convert numeric values
- write the final structured results to `books_pipeline.json`
- preserve a richer dataset than the base listing-only scraper

## Day 13 - Data cleaning, validation, and export

- the spider yields raw book items from the listing and detail pages
- `BookcrawlerPipeline` cleans strings and converts price/review values
- `BookValidationPipeline` ensures required fields and sensible numeric values exist
- `DuplicateBookPipeline` tracks UPCs and skips repeated books
- the cleaned dataset is exported as a final JSON file for analysis

## Run Day 13 Script

```bash
cd scrapy_projects\bookcrawler
scrapy crawl books -o books_pipeline.json
```

## What the Day 13 Script Does

- runs the spider end-to-end from list page to detail page
- sends each scraped item through the cleaning pipeline
- validates fields before accepting the item for export
- removes duplicate books using UPC tracking
- writes the final validated dataset to `books_pipeline.json`
- prepares the data for later analysis and reporting

## Day 14 - Scrapy callback passing patterns

### `response.follow()`

For following links:

```python
yield response.follow(url, callback=self.parse_detail)
```

### `meta`

For request/response metadata:

```python
meta={"some_data": value}
```

### `cb_kwargs`

For explicitly passing callback arguments:

```python
cb_kwargs={"title": title}
```

And you've learned the important architectural distinction:

```text
Listing page
    ↓
Discovery / navigation
    ↓
Detail URL
    ↓
Detail page
    ↓
Authoritative extraction
    ↓
Item
```

This is a solid Scrapy pattern for structured detail-page scraping.

## Day 15: Concurrency, Retry & Middleware

- Scrapy can send many requests in parallel to improve crawl speed
- concurrency settings control how aggressively the spider requests pages
- retries help recover from temporary network or server problems
- middleware sits in the request/response pipeline and can modify behavior globally
- this is important for resilience, rate control, and custom request handling

## Run Day 15 Example

```bash
cd scrapy_projects\bookcrawler
scrapy crawl books
```

## What the Day 15 Topic Covers

- how Scrapy handles concurrency during a crawl
- what retry behavior looks like for failed requests
- where middleware fits in the request lifecycle
- how to make crawlers more stable and production-ready for real-world sites

## Notes

This is a learning project. Use scraping responsibly and respect the website's rules.
