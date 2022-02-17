import os
import warnings

import alembic
import pytest
import pytest_asyncio
from alembic.config import Config
from app.db.repositories.books import BookRepository
from app.models.book import BookCreate, BookResponse, BookUpdate
from asgi_lifespan import LifespanManager
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient


@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.api.server import get_application

    return get_application()


@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client


@pytest.fixture
def new_book():
    return BookCreate(
        isbn10="0000000000",
        isbn13="0000000000000",
        title="test book",
        description="test description",
        authors=["John Doe"],
        categories=["Literature"],
        page_count=123,
        published_date="2022-01-01",
    )


@pytest.fixture
async def test_book(db: Database) -> BookResponse:
    book_repo = BookRepository(db)
    new_book = BookCreate(
        isbn10="000000000X",
        isbn13="0000000000001",
        title="fake book title",
        description="fake book description",
        authors=["fake author"],
        categories=["fake category"],
        page_count=0,
        published_date="1900-01-01",
    )
    return await book_repo.create_book(new_book=new_book)


@pytest.fixture
def update_data():
    return BookUpdate(
        title="new test book",
        page_count=500,
    )
