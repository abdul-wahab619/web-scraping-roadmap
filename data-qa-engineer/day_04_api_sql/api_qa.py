import requests

API_URL = "https://jsonplaceholder.typicode.com/posts"


def validate_api():
    print("========== API QA REPORT ==========\n")

    # Initialize report values
    status_code = None
    response_valid = False
    total_records = 0

    missing_ids = 0
    missing_titles = 0
    missing_bodies = 0
    missing_user_ids = 0
    duplicate_ids = 0

    try:
        # 1. Send GET request
        response = requests.get(API_URL, timeout=10)

        status_code = response.status_code

        # 2. Check HTTP status
        if status_code != 200:
            print(f"HTTP Status: {status_code}")
            print("API request failed.")
            return

        # 3. Validate JSON response
        try:
            data = response.json()
            response_valid = True
        except ValueError:
            print(f"HTTP Status: {status_code}")
            print("Response Valid: False")
            print("Invalid JSON response.")
            return

        # 4. Confirm response is a list
        if not isinstance(data, list):
            print(f"HTTP Status: {status_code}")
            print(f"Response Valid: {response_valid}")
            print("Response is not a list.")
            return

        total_records = len(data)

        # Track post IDs
        seen_ids = set()

        # 5. Validate each post
        for post in data:

            if not isinstance(post, dict):
                missing_ids += 1
                missing_titles += 1
                missing_bodies += 1
                missing_user_ids += 1
                continue

            if post.get("id") is None:
                missing_ids += 1

            if post.get("title") is None:
                missing_titles += 1

            if post.get("body") is None:
                missing_bodies += 1

            if post.get("userId") is None:
                missing_user_ids += 1

            # 6. Detect duplicate IDs
            post_id = post.get("id")

            if post_id is not None:
                if post_id in seen_ids:
                    duplicate_ids += 1
                else:
                    seen_ids.add(post_id)

        # 7. Print QA report
        print(f"HTTP Status: {status_code}")
        print(f"Response Valid: {response_valid}")
        print(f"Total Records: {total_records}")

        print(f"\nMissing IDs: {missing_ids}")
        print(f"Missing Titles: {missing_titles}")
        print(f"Missing Bodies: {missing_bodies}")
        print(f"Missing User IDs: {missing_user_ids}")
        print(f"Duplicate IDs: {duplicate_ids}")

    except requests.exceptions.RequestException as error:
        print(f"API Request Error: {error}")


if __name__ == "__main__":
    validate_api()
