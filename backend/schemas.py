from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str
    price: float | None = None
    rating: int | None = None
    url: str
    upc: str
    product_type: str | None = None
    price_excl_tax: float | None = None
    price_incl_tax: float | None = None
    tax: float | None = None
    availability: str | None = None
    number_of_reviews: int | None = None
    description: str | None = None


class BooksResponse(BaseModel):
    count: int
    limit: int
    offset: int
    books: list[Book]
