# The following Python script calculates validity and invalidity percentages and provides a final QA recommendation.


def generate_qa_summary(total_records, valid_records, invalid_records):

    if total_records <= 0:
        raise ValueError("Total records must be greater than zero.")

    if valid_records < 0 or invalid_records < 0:
        raise ValueError("Record counts cannot be negative.")

    if valid_records + invalid_records != total_records:
        raise ValueError("Record counts must match the total.")

    validity_percentage = (valid_records / total_records) * 100

    invalidity_percentage = (invalid_records / total_records) * 100

    print("===== SCRAPER QA SUMMARY =====")

    print(f"Total Records: {total_records}")
    print(f"Valid Records: {valid_records}")
    print(f"Invalid Records: {invalid_records}")

    print(f"Validity: {validity_percentage:.2f}%")
    print(f"Invalidity: {invalidity_percentage:.2f}%")

    if validity_percentage >= 95:
        recommendation = "PASS - Data quality is acceptable."
    elif validity_percentage >= 90:
        recommendation = "CONDITIONAL PASS - Fix invalid records before release."
    else:
        recommendation = "FAIL - Data quality needs improvement."

    print(f"QA Recommendation: {recommendation}")


# Example inputs
total_records = 1000
valid_records = 920
invalid_records = 80

generate_qa_summary(total_records, valid_records, invalid_records)
