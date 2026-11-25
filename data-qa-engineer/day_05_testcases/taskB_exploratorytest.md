Task B: Exploratory Testing

I would perform the following additional tests to identify unexpected scraper issues.

1. Website HTML Structure Change

Inspect: Check whether product cards still use the expected HTML tags and CSS selectors.

Expected failure: The scraper returns missing fields or empty records when website selectors change.

2. Network Connection Failure

Inspect: Disconnect the network or simulate a timeout while scraping.

Expected failure: Requests fail, and the scraper does not retry or recover properly.

3. Unexpected Price Format

Inspect: Check prices containing commas, currency symbols, spaces, or decimal values.

Expected failure: The scraper incorrectly converts prices or stores invalid values.

4. Pagination Loop

Inspect: Check whether the scraper follows next-page links correctly and stops at the last page.

Expected failure: Some pages are skipped, or the scraper repeatedly visits the same page.

5. Inconsistent Product Records

Inspect: Compare repeated product records across different pages.

Expected failure: Duplicate products are stored, or updated product information is handled incorrectly.
