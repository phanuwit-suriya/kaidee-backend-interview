from typing import Optional, List

from ...db.repositories.base import BaseRepository
from ...models.book import BookCreate, BookResponse, BookUpdate

CREATE_BOOK_QUERY = """
INSERT INTO books (isbn10, isbn13, title, description, authors, categories, page_count, published_date)
VALUES (:isbn10, :isbn13, :title, :description, :authors, :categories, :page_count, :published_date)
RETURNING *;
"""

GET_BOOK_BY_ID_QUERY = """
SELECT id, isbn10, isbn13, title, description, authors, categories, page_count, published_date
FROM books
WHERE id = :id;
"""

GET_BOOKS_QUERY = """
SELECT id, isbn10, isbn13, title, description, authors, categories, page_count, published_date
FROM books
ORDER BY id
LIMIT :limit
OFFSET :offset;
"""

UPDATE_BOOKS_QUERY = """
UPDATE books 
SET isbn10 = :isbn10, isbn13 = :isbn13, title = :title, description = :description, authors = :authors,
    categories = :categories, page_count = :page_count, published_date = :published_date
WHERE id = :id
RETURNING *; 
"""

DELETE_BOOK_QUERY = """
DELETE FROM books WHERE id = :id RETURNING *;
"""


class BookRepository(BaseRepository):
    async def create_book(self, *, new_book: BookCreate) -> BookResponse:
        query_value = new_book.dict()
        created_book = await self.db.fetch_one(
            query=CREATE_BOOK_QUERY, values=query_value
        )
        return BookResponse(**created_book)

    async def get_book_by_id(self, *, id: int) -> Optional[BookResponse]:
        book = await self.db.fetch_one(query=GET_BOOK_BY_ID_QUERY, values={"id": id})
        if not book:
            return None
        return BookResponse(**book)

    async def get_books(
        self, *, limit: int, offset: int
    ) -> Optional[List[BookResponse]]:
        books = await self.db.fetch_all(
            query=GET_BOOKS_QUERY, values={"limit": limit, "offset": offset}
        )
        if not books:
            return None
        return [BookResponse(**book) for book in books]

    async def update_book(
        self, *, id: int, update_data: BookUpdate
    ) -> Optional[BookResponse]:
        book_in_db = await self.db.fetch_one(
            query=GET_BOOK_BY_ID_QUERY, values={"id": id}
        )
        if not book_in_db:
            return None
        book = BookResponse(**book_in_db)
        update = book.copy(update=update_data.dict(exclude_unset=True))
        query_value = update.dict()
        updated_book = await self.db.fetch_one(
            query=UPDATE_BOOKS_QUERY, values=query_value
        )
        return BookResponse(**updated_book)

    async def delete_book(self, *, id: int) -> Optional[BookResponse]:
        deleted_book = await self.db.fetch_one(
            query=DELETE_BOOK_QUERY, values={"id": id}
        )
        if not deleted_book:
            return None
        return BookResponse(**deleted_book)
