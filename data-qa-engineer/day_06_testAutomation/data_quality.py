import pandas as pd

# 1. Load CSV
df = pd.read_csv("products.csv")

# 2. Count total records
total_records = len(df)

print("===== DATA QUALITY REPORT =====")
print(f"Total records: {total_records}")

# 3. Detect missing values
missing_values = df.isnull().sum()

print("\nMissing values:")
print(missing_values)
print(f"Total missing values: {df.isnull().sum().sum()}")

# 4. Detect duplicate product IDs
duplicate_ids = df["product_id"].duplicated(keep=False)

print(f"\nDuplicate product IDs: {duplicate_ids.sum()}")

# 5. Find invalid prices
df["price"] = pd.to_numeric(df["price"], errors="coerce")

invalid_prices = df["price"].isna() | (df["price"] <= 0)

print(f"Invalid prices: {invalid_prices.sum()}")

# 6. Find ratings outside 0–5
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

invalid_ratings = df["rating"].notna() & ((df["rating"] < 0) | (df["rating"] > 5))

print(f"Invalid ratings: {invalid_ratings.sum()}")

# 7. Identify all invalid records
missing_records = df.isnull().any(axis=1)

invalid_mask = missing_records | duplicate_ids | invalid_prices | invalid_ratings

invalid_records = df[invalid_mask].copy()

valid_records = df[~invalid_mask]

validity_percentage = (
    len(valid_records) / total_records * 100 if total_records > 0 else 0
)

print(f"\nValid records: {len(valid_records)}")
print(f"Invalid records: {len(invalid_records)}")
print(f"Validity percentage: {validity_percentage:.2f}%")

# 8. Save invalid records
invalid_records.to_csv("invalid_records.csv", index=False)

print("\nInvalid records saved to invalid_records.csv")
print("===== ANALYSIS COMPLETED =====")
