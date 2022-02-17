from typing import Optional, List

from ...db.repositories.base import BaseRepository
from ...models.history import BorrowingHistory, ReturningHistory, HistoryResponse

GET_BOOK_LATEST_HISTORY_QUERY = """
SELECT id, book_id, borrowing_date, returning_date
FROM histories
WHERE book_id = :book_id
ORDER BY borrowing_date DESC, returning_date DESC
LIMIT 1;
"""

BORROW_BOOK_QUERY = """
INSERT INTO histories (book_id, borrowing_date, returning_date)
VALUES (:book_id, :borrowing_date, :returning_date)
RETURNING *;
"""

RETURN_BOOK_QUERY = """
UPDATE histories
SET returning_date = :returning_date
WHERE id = :id AND book_id = :book_id AND borrowing_date = :borrowing_date
RETURNING *;
"""

GET_BOOK_HISTORIES_QUERY = """
SELECT book_id, borrowing_date, returning_date
FROM histories
WHERE book_id = :book_id
ORDER BY borrowing_date DESC, returning_date DESC
"""


class HistoryRepository(BaseRepository):
    async def get_book_latest_history(self, *, book_id: int) -> Optional[HistoryResponse]:
        history = await self.db.fetch_one(
            query=GET_BOOK_LATEST_HISTORY_QUERY, values={"book_id": book_id}
        )
        if not history:
            return None
        return HistoryResponse(**history)

    async def borrow_book(
        self, *, borrowing_history: BorrowingHistory
    ) -> HistoryResponse:
        query_value = borrowing_history.dict()
        created_history = await self.db.fetch_one(
            query=BORROW_BOOK_QUERY, values=query_value
        )
        return HistoryResponse(**created_history)

    async def return_book(
        self, *, returning_history: ReturningHistory
    ) -> Optional[HistoryResponse]:
        query_value = returning_history.dict()
        updated_history = await self.db.fetch_one(
            query=RETURN_BOOK_QUERY, values=query_value
        )
        return HistoryResponse(**updated_history)

    async def get_borrow_history(self, *, book_id: int) -> Optional[List[HistoryResponse]]:
        histories = await self.db.fetch_all(query=GET_BOOK_HISTORIES_QUERY, values={"book_id": book_id})
        if not histories:
            return None
        return [HistoryResponse(**history) for history in histories]
