import pytest
from app.models.book import BookCreate, BookResponse, BookUpdate
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

pytestmark = pytest.mark.asyncio


class TestBooksRoutes:
    @pytestmark
    async def test_create_book_route_exist(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post(app.url_path_for("books:create-book"), json={})
        assert res.status_code != status.HTTP_404_NOT_FOUND

    @pytestmark
    async def test_get_book_by_id_route_exist(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.get(app.url_path_for("books:get-book-by-id", id=None))
        assert res.status_code != status.HTTP_404_NOT_FOUND

    @pytestmark
    async def test_get_books_route_exist(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.get(app.url_path_for("books:get-books"))
        assert res.status_code != status.HTTP_404_NOT_FOUND

    @pytestmark
    async def test_update_book_route_exist(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.patch(
            app.url_path_for("books:update-book", id=None), json={}
        )
        assert res.status_code != status.HTTP_404_NOT_FOUND

    @pytestmark
    async def test_delete_book_route_exist(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.delete(app.url_path_for("books:delete-book", id=None))
        assert res.status_code != status.HTTP_404_NOT_FOUND


class TestCreateBook:
    async def test_valid_input_create_book(
        self, app: FastAPI, client: AsyncClient, new_book: BookCreate
    ) -> None:
        res = await client.post(
            app.url_path_for("books:create-book"), json={"new_book": new_book.dict()}
        )
        assert res.status_code == status.HTTP_201_CREATED
        created_book = BookCreate(**res.json())
        assert created_book == new_book

    @pytest.mark.parametrize(
        "invalid_payload, status_code",
        (
            (None, 422),
            ({}, 422),
            ({"title": None}, 422),
            ({"page_count": 123.45}, 422),
            ({"title": None, "description": "test description"}, 422),
        ),
    )
    async def test_invalid_input_raise_error(
        self, app: FastAPI, client: AsyncClient, invalid_payload: dict, status_code: int
    ) -> None:
        res = await client.post(
            app.url_path_for("books:create-book"), json={"new_book": invalid_payload}
        )
        assert res.status_code == status_code


class TestGetBook:
    async def test_get_book_by_id(
        self, app: FastAPI, client: AsyncClient, test_book: BookResponse
    ) -> None:
        res = await client.get(
            app.url_path_for("books:get-book-by-id", id=test_book.id)
        )
        assert res.status_code == status.HTTP_200_OK
        book = BookResponse(**res.json())
        assert book.id == 12

    @pytest.mark.parametrize(
        "id, status_code",
        (
            (500, 404),
            (-1, 404),
            (None, 422),
        ),
    )
    async def test_wrong_id_return_error(
        self, app: FastAPI, client: AsyncClient, id: int, status_code: int
    ) -> None:
        res = await client.get(app.url_path_for("books:get-book-by-id", id=id))
        assert res.status_code == status_code


class TestUpdateBook:
    async def test_update_book(
        self, app: FastAPI, client: AsyncClient, update_data: BookUpdate
    ) -> None:
        res = await client.patch(
            app.url_path_for("books:update-book", id=12),
            json={"update_data": update_data.dict()},
        )
        assert res.status_code == status.HTTP_200_OK
        updated_book = BookUpdate(**res.json())
        assert updated_book.title == update_data.title
        assert updated_book.page_count == update_data.page_count

    @pytest.mark.parametrize(
        "id, payload, status_code",
        (
            (12, None, 422),
            (50, {"title": "new title"}, 404),
        ),
    )
    async def test_invalid_input_raise_error(
        self,
        app: FastAPI,
        client: AsyncClient,
        id: int,
        payload: dict,
        status_code: int,
    ) -> None:
        res = await client.patch(
            app.url_path_for("books:update-book", id=id),
            json={"update_data": payload},
        )
        assert res.status_code == status_code


class TestDeleteBook:
    async def test_delete_book(self, app: FastAPI, client: AsyncClient):
        res = await client.delete(app.url_path_for("books:delete-book", id=12))
        assert res.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize(
        "id, status_code",
        ((12, 410),),
    )
    async def test_invalid_input_raise_error(
        self, app: FastAPI, client: AsyncClient, id: int, status_code: int
    ) -> None:
        res = await client.delete(app.url_path_for("books:delete-book", id=id))
        assert res.status_code == status_code
