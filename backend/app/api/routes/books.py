import datetime
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from starlette import status

from ...api.dependencies.database import get_repository
from ...db.repositories.books import BookRepository
from ...db.repositories.histories import HistoryRepository
from ...models.book import BookResponse, BookCreate, BookUpdate
from ...models.history import HistoryResponse, BorrowingHistory, ReturningHistory

router = APIRouter()


@router.post(
    "/",
    response_model=BookResponse,
    name="books:create-book",
    status_code=status.HTTP_201_CREATED,
)
async def create_book(
    new_book: BookCreate = Body(..., embed=True),
    book_repo: BookRepository = Depends(get_repository(BookRepository)),
) -> BookResponse:
    created_book = await book_repo.create_book(new_book=new_book)
    return created_book


@router.get(
    "/{id}",
    response_model=BookResponse,
    name="books:get-book-by-id",
    status_code=status.HTTP_200_OK,
)
async def get_book_by_id(
    id: int, book_repo: BookRepository = Depends(get_repository(BookRepository))
) -> BookResponse:
    book = await book_repo.get_book_by_id(id=id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No book found with that id."
        )
    return book


@router.get(
    "/",
    response_model=List[BookResponse],
    name="books:get-books",
    status_code=status.HTTP_200_OK,
)
async def get_books(
    limit: int = 10,
    offset: int = 0,
    book_repo: BookRepository = Depends(get_repository(BookRepository)),
) -> List[BookResponse]:
    books = await book_repo.get_books(limit=limit, offset=offset)
    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No books found,",
        )
    return books


@router.patch(
    "/{id}",
    response_model=BookResponse,
    name="books:update-book",
    status_code=status.HTTP_200_OK,
)
async def update_book(
    id: int,
    update_data: BookUpdate = Body(..., embed=True),
    book_repo: BookRepository = Depends(get_repository(BookRepository)),
) -> BookResponse:
    updated_book = await book_repo.update_book(id=id, update_data=update_data)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No book found with that id."
        )
    return updated_book


@router.delete(
    "/{id}",
    response_model=BookResponse,
    name="books:delete-book",
    status_code=status.HTTP_200_OK,
)
async def delete_book(
    id: int, book_repo: BookRepository = Depends(get_repository(BookRepository))
) -> BookResponse:
    deleted_book = await book_repo.delete_book(id=id)
    if not deleted_book:
        raise HTTPException(
            status_code=status.HTTP_410_GONE, detail="No book found with that id."
        )
    return deleted_book


@router.post(
    "/{id}/burrow",
    response_model=HistoryResponse,
    name="books:burrow-book",
    status_code=status.HTTP_200_OK,
)
async def burrow_book(
    id: int,
    book_repo: BookRepository = Depends(get_repository(BookRepository)),
    history_repo: HistoryRepository = Depends(get_repository(HistoryRepository)),
) -> HistoryResponse:
    book = await book_repo.get_book_by_id(id=id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No book found with that id."
        )

    latest_history = await history_repo.get_book_latest_history(book_id=id)
    if latest_history and not latest_history.returning_date:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Cannot burrow this book."
        )

    borrowing_history = BorrowingHistory(
        book_id=id, borrowing_date=datetime.datetime.utcnow()
    )
    return await history_repo.borrow_book(borrowing_history=borrowing_history)


@router.post(
    "/{id}/return",
    response_model=HistoryResponse,
    name="books:return-book",
    status_code=status.HTTP_200_OK,
)
async def return_book(
    id: int,
    book_repo: BookRepository = Depends(get_repository(BookRepository)),
    history_repo: HistoryRepository = Depends(get_repository(HistoryRepository)),
) -> HistoryResponse:
    book = await book_repo.get_book_by_id(id=id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No book found with that id."
        )

    latest_history = await history_repo.get_book_latest_history(book_id=id)
    if not latest_history or latest_history.returning_date:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Cannot return this book."
        )
    history = latest_history.dict()
    returning_history = ReturningHistory(
        id=history["id"],
        book_id=history["book_id"],
        borrowing_date=history["borrowing_date"],
        returning_date=datetime.datetime.utcnow(),
    )
    return await history_repo.return_book(returning_history=returning_history)


@router.get(
    "/{id}/burrow-history",
    response_model=List[HistoryResponse],
    name="books:burrow-history",
    status_code=status.HTTP_200_OK,
)
async def get_burrow_history(
    id: int,
    history_repo: HistoryRepository = Depends(get_repository(HistoryRepository)),
) -> List[HistoryResponse]:
    histories = await history_repo.get_borrow_history(book_id=id)
    if not histories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No book's burrow history found,",
        )
    return histories
