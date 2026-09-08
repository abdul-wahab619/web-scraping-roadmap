import json

#load books from JSON

with open("books.json", "r", encoding="utf-8") as file:
    books = json.load(file)
    

# print total number of books loaded from JSON
print(f"\nTotal books loaded from JSON: {len(books)}")


# calculate total price and average price of books loaded from JSON
total_price = sum(book["price"] for book in books)

average_price = total_price / len(books)

print("Average price:", average_price)

# find the book with the highest price
most_expensive_book = max(books, key=lambda book: book["price"])

print("\nMost expensive book:")
print("Title:", most_expensive_book["title"])
print("Price:", most_expensive_book["price"])

# find the book with the lowest price

most_affordable_book = min(books, key=lambda book: book["price"])

print("\nMost affordable book:")
print("Title:", most_affordable_book["title"])
print("Price:", most_affordable_book["price"])


# average rating of books loaded from JSON

total_rating = sum(book["rating"] for book in books)
average_rating = total_rating / len(books)

print(f"\nAverage rating: {average_rating:.2f}")