import datetime
from typing import Optional

from ..models.core import CoreModel


class BaseHistory(CoreModel):
    borrowing_date: Optional[datetime.datetime]
    returning_date: Optional[datetime.datetime]


class BorrowingHistory(BaseHistory):
    book_id: int
    borrowing_date: datetime.datetime


class ReturningHistory(BaseHistory):
    id: int
    book_id: int
    borrowing_date: datetime.datetime
    returning_date: datetime.datetime


class HistoryResponse(BaseHistory):
    pass
