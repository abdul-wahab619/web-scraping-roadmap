from datetime import datetime, timezone

from bookcrawler.items import JobItem
from bookcrawler.pipelines import JobValidationPipeline

pipeline = JobValidationPipeline()


def create_job(**overrides):
    data = {
        "title": "Software Engineer",
        "company": "Test Company",
        "location": "Remote",
        "job_type": "Full-time",
        "remote": True,
        "salary": None,
        "description": "Test job",
        "url": "https://example.com/job/123",
        "source": "test",
        "external_id": "123",
        "posted_at": None,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
    }

    data.update(overrides)

    return JobItem(**data)


tests = [
    (
        "Missing title",
        create_job(title=None),
    ),
    (
        "Invalid URL",
        create_job(url="not-a-url"),
    ),
    (
        "Missing source",
        create_job(source=None),
    ),
    (
        "Missing external_id",
        create_job(external_id=None),
    ),
    (
        "Missing scraped_at",
        create_job(scraped_at=None),
    ),
    (
        "Invalid remote value",
        create_job(remote="yes"),
    ),
]


for test_name, item in tests:
    try:
        pipeline.process_item(item)
        print(f"❌ FAILED: {test_name} was accepted")

    except Exception as e:
        print(f"✅ PASSED: {test_name} → {e}")

valid_item = create_job()

try:
    result = pipeline.process_item(valid_item)

    if result is valid_item:
        print("✅ PASSED: Valid job accepted")
    else:
        print("❌ FAILED: Valid job was modified or replaced")

except Exception as e:
    print(f"❌ FAILED: Valid job was rejected → {e}")
