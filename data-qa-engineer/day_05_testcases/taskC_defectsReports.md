Task C: Defect Reports

Bug Report 1: Missing Required Product Fields

Bug ID: BUG-001

Title: Scraper accepts products with missing title, price, and URL.

Environment: Python Scrapy, Windows 11, Test Environment

Severity: High

Priority: High

Description:

The scraper extracts a Tablet product with missing title, price, and product URL. These fields are required by the customer, but the incomplete record is not properly rejected or reported.

Steps to Reproduce:

Open the product listing page.

Run the product scraper.

Inspect the extracted Tablet record.

Expected Result:

The scraper should detect missing required fields and reject the incomplete record or report a data quality error.

Actual Result:

The incomplete Tablet record is extracted without all required fields.

Business Impact:

Incomplete product information can affect customer reports, product listings, and downstream data processing.

Evidence:

Extracted Tablet record:

{
"title": None,
"price": None,
"availability": "In Stock",
"url": None
}

Bug Report 2: Duplicate Product URLs

Bug ID: BUG-002

Title: Scraper stores duplicate product records with the same URL.

Environment: Python Scrapy, Windows 11, Test Environment

Severity: Medium

Priority: Medium

Description:

The scraper stores the same product URL multiple times. This creates duplicate product records in the output dataset.

Steps to Reproduce:

Run the scraper on multiple product listing pages.

Collect all extracted product URLs.

Check the output for duplicate URLs.

Expected Result:

Each product URL should appear only once in the final dataset.

Actual Result:

The same product URL appears multiple times in the extracted records.

Business Impact:

Duplicate records can affect product counts, reporting accuracy, and database consistency.

Evidence:

product_urls = [
"https://example.com/laptop",
"https://example.com/phone",
"https://example.com/laptop"
]

Expected unique records: 2

Actual records: 3

Note: BUG-001 is based on the supplied sample data. BUG-002 is a realistic simulated defect for testing purposes.
