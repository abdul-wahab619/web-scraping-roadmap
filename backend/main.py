from fastapi import FastAPI, Query, HTTPException
from database import get_connection
from schemas import BooksResponse, Book
from redis_client import redis_client
from datetime import datetime, timezone
import uuid

app = FastAPI(
    title="BookCrawler API",
    version="1.0.0",
)


def row_to_book(row):
    return {
        "id": row[0],
        "title": row[1],
        "price": float(row[2]) if row[2] is not None else None,
        "rating": row[3],
        "url": row[4],
        "upc": row[5],
        "product_type": row[6],
        "price_excl_tax": (float(row[7]) if row[7] is not None else None),
        "price_incl_tax": (float(row[8]) if row[8] is not None else None),
        "tax": float(row[9]) if row[9] is not None else None,
        "availability": row[10],
        "number_of_reviews": row[11],
        "description": row[12],
    }


@app.get("/")
def root():
    return {"message": "BookCrawler API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/redis/health")
def redis_health():
    redis_client.set("test_key", "Redis is working")
    value = redis_client.get("test_key")
    return {
        "status": "ok",
        "value": value,
    }


@app.post("/scrape")
def create_scrape_job():
    job_id = str(uuid.uuid4())

    job_key = f"scrape_job:{job_id}"
    created_at = datetime.now(timezone.utc).isoformat()

    redis_client.hset(
        job_key,
        mapping={"job_id": job_id, "status": "queued", "created_at": created_at},
    )
    redis_client.lpush("scrape_queue", job_id)
    return {
        "job_id": job_id,
        "status": "queued",
    }


@app.get("/scrape/{job_id}")
def get_scrape_job(job_id: str):
    job_key = f"scrape_job:{job_id}"

    job = redis_client.hgetall(job_key)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Scrape job not found",
        )

    return job


@app.get("/books/count")
def books_count():

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM books")

            result = cursor.fetchone()

            return {"count": result[0]}

    finally:
        connection.close()


@app.get("/books", response_model=BooksResponse)
def get_books(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    rating: int | None = Query(default=None, ge=1, le=5),
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
):
    # Validate price range
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=400,
            detail="min_price cannot be greater than max_price",
        )

    # Build dynamic WHERE conditions
    conditions = []
    parameters = []

    if rating is not None:
        conditions.append("rating = %s")
        parameters.append(rating)

    if min_price is not None:
        conditions.append("price >= %s")
        parameters.append(min_price)

    if max_price is not None:
        conditions.append("price <= %s")
        parameters.append(max_price)

    where_clause = ""

    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT
                    id,
                    title,
                    price,
                    rating,
                    url,
                    upc,
                    product_type,
                    price_excl_tax,
                    price_incl_tax,
                    tax,
                    availability,
                    number_of_reviews,
                    description
                FROM books
                {where_clause}
                ORDER BY id
                LIMIT %s
                OFFSET %s
                """,
                (*parameters, limit, offset),
            )

            rows = cursor.fetchall()

            books = [row_to_book(row) for row in rows]

            return {
                "count": len(books),
                "limit": limit,
                "offset": offset,
                "books": books,
            }

    finally:
        connection.close()


@app.get("/books/search", response_model=BooksResponse)
def search_books(
    q: str = Query(min_length=1),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    title,
                    price,
                    rating,
                    url,
                    upc,
                    product_type,
                    price_excl_tax,
                    price_incl_tax,
                    tax,
                    availability,
                    number_of_reviews,
                    description
                FROM books
                WHERE title ILIKE %s
                   OR description ILIKE %s
                ORDER BY id
                LIMIT %s
                OFFSET %s
                """,
                (
                    f"%{q}%",
                    f"%{q}%",
                    limit,
                    offset,
                ),
            )

            rows = cursor.fetchall()

            books = [row_to_book(row) for row in rows]

            return {
                "count": len(books),
                "limit": limit,
                "offset": offset,
                "books": books,
            }

    finally:
        connection.close()


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    title,
                    price,
                    rating,
                    url,
                    upc,
                    product_type,
                    price_excl_tax,
                    price_incl_tax,
                    tax,
                    availability,
                    number_of_reviews,
                    description
                FROM books
                WHERE id = %s
                """,
                (book_id,),
            )

            row = cursor.fetchone()

            if row is None:
                raise HTTPException(
                    status_code=404,
                    detail="Book not found",
                )

            return row_to_book(row)

    finally:
        connection.close()
