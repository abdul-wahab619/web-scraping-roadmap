# Historical product counts
historical_counts = [1000, 1010, 995, 1005, 1002, 998]

# Latest scraper run
current_count = 420

# Anomaly threshold
threshold = 80  # 80% of historical average

# Calculate historical average
historical_average = sum(historical_counts) / len(historical_counts)

# Calculate percentage of expected records
current_percentage = (current_count / historical_average) * 100

# Calculate percentage drop
percentage_drop = 100 - current_percentage

# Print report
print("===== ANOMALY DETECTION REPORT =====")

print(f"Historical average: {historical_average:.2f}")
print(f"Current product count: {current_count}")
print(f"Expected minimum count: {historical_average * threshold / 100:.2f}")
print(f"Percentage of expected records: {current_percentage:.2f}%")
print(f"Percentage drop: {percentage_drop:.2f}%")

# Detect anomaly
if current_percentage < threshold:
    print("\nSTATUS: ANOMALY DETECTED")
    print(
        f"Reason: Product count dropped by {percentage_drop:.2f}%, "
        f"exceeding the allowed 20% drop."
    )
else:
    print("\nSTATUS: NORMAL")
    print("Product count is within the acceptable range.")

print("===== ANALYSIS COMPLETED =====")