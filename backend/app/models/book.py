from typing import Optional, List

from ..models.core import CoreModel, ResponseModelMixin


class BaseBook(CoreModel):
    isbn10: Optional[str]
    isbn13: Optional[str]
    title: Optional[str]
    description: Optional[str]
    authors: Optional[List[str]]
    categories: Optional[List[str]]
    page_count: Optional[int]
    published_date: Optional[str]


class BookCreate(BaseBook):
    title: str


class BookUpdate(BaseBook):
    pass


class BookResponse(BaseBook, ResponseModelMixin):
    pass
