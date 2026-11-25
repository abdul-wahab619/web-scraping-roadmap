# Task A: Design test cases
# Create at least 10 test cases covering:
# - Valid product extraction.
# - Missing title.
# - Missing price.
# - Invalid price.
# - Missing URL.
# - Invalid rating.
# - Duplicate product URL.
# - Unexpected availability value.
# - Pagination failure.
# - Empty extraction result.


test_cases = [
    {
        "id": "TC-001",
        "scenario": "Validate product title extraction",
        "test_data": {"title": "Laptop"},
        "expected_result": "Pass",
        "actual_result": None,
        "status": "Not Executed",
    },
    {
        "id": "TC-002",
        "scenario": "Validate missing product title",
        "test_data": {"title": None},
        "expected_result": "Fail - Missing title should be detected",
        "actual_result": None,
        "status": "Not Executed",
    },
    {
        "id": "TC-003",
        "scenario": "Validate missing product price",
        "test_data": {"price": None},
        "expected_result": "Fail - Missing price should be detected",
        "actual_result": None,
        "status": "Not Executed",
    },
    {
        "id": "TC-004",
        "scenario": "Validate invalid product price",
        "test_data": {"price": "ABC"},
        "expected_result": "Fail - Invalid price should be rejected",
        "actual_result": None,
        "status": "Not Executed",
    },
    {
        "id": "TC-005",
        "scenario": "Validate missing product URL",
        "test_data": {"url": None},
        "expected_result": "Fail - Missing URL should be detected",
        "actual_result": None,
        "status": "Not Executed",
    },
    {
        "id": "TC-006",
        "scenario": "Validate invalid product rating",
        "test_data": {"rating": 7},
        "expected_result": "Fail - Rating must be between 1 and 5",
        "actual_result": None,
        "status": "Not Executed",
    },
    {
        "id": "TC-007",
        "scenario": "Check duplicate product URLs",
        "test_data": {
            "urls": ["https://example.com/laptop", "https://example.com/laptop"]
        },
        "expected_result": "Fail - Duplicate product URL should be detected",
        "actual_result": None,
        "status": "Not Executed",
    },
    {
        "id": "TC-008",
        "scenario": "Validate unexpected availability value",
        "test_data": {"availability": "Coming Soon"},
        "expected_result": "Fail - Unexpected availability value should be flagged",
        "actual_result": None,
        "status": "Not Executed",
    },
    {
        "id": "TC-009",
        "scenario": "Validate pagination functionality",
        "test_data": {"expected_pages": 3, "scraped_pages": 2},
        "expected_result": "Fail - All expected pages must be scraped",
        "actual_result": None,
        "status": "Not Executed",
    },
    {
        "id": "TC-010",
        "scenario": "Validate empty extraction result",
        "test_data": {"products": []},
        "expected_result": "Fail - Empty extraction should be reported",
        "actual_result": None,
        "status": "Not Executed",
    },
]
