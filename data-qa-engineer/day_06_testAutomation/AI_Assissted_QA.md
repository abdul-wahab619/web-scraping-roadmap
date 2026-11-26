Generate five additional test cases for a product scraper.

## The scraper collects:
- Product title
- Product price
- Availability
- Product URL

## Requirements:
- Title must not be empty.
- Price must be numeric and greater than 0.
- Availability must be either In Stock or Out of Stock.
- Product URL must be valid.

## For each test case, provide:
1. Test case name
2. Test data or scenario
3. Expected result
4. Reason why the test is important.

Include both positive and negative test cases. Avoid testing features outside these requirements.


# Scenario of test cases:
Five AI-generated test cases
Here are five example test cases generated from the prompt.
## Test Case 1: Missing Product Title
Relevant
- Input: Title is empty.
- Expected: Record should fail validation.
- Why useful: Ensures incomplete product records are not accepted.

## Test Case 2: Negative Product Price
Relevant
- Input: Price = -50.
- Expected: Record should fail validation.
- Why useful: Prevents invalid prices from entering the dataset.

## Test Case 3: Invalid Product URL
Relevant
- Input: URL = htp:/product123.
- Expected: Record should fail URL validation.
- Why useful: Ensures every product has a valid URL.

## Test Case 4: Invalid Availability
Relevant
- Input: Availability = Coming Soon.
- Expected: Record should fail validation.
- Why useful: Ensures availability contains only the two permitted values.

## Test Case 5: Product Image Download
Out of scope
- Input: Product image URL is unavailable.
- Expected: Scraper should retry downloading the image three times.
- Why useful: Could help test image downloading functionality.
- Issue: Image downloading and retry behavior are not part of the stated scraper requirements.


# Final QA Review:

### AI-Assisted QA Review

I used an AI tool to generate five additional test cases for the product scraper.

After reviewing the generated cases, I found that four were relevant to the defined requirements. They covered missing product titles, negative prices, invalid URLs, and unsupported availability values.

The fifth test case focused on product image downloading and retry behavior. I rejected it because image downloading is not included in the scraper requirements.

**Conclusion:** AI can help generate test ideas quickly, but every generated test case must be reviewed against actual project requirements before implementation.