"""create_main_tables

Revision ID: 76996beafe24
Revises: 
Create Date: 2022-02-16 03:51:15.879049

"""
import requests
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic
revision = "76996beafe24"
down_revision = None
branch_labels = None
depends_on = None
url = "https://www.googleapis.com/books/v1/volumes?q=%E0%B9%80%E0%B8%A5%E0%B8%82ISBN"


def create_books_table():
    return op.create_table(
        "books",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("isbn10", sa.VARCHAR(10), nullable=True, unique=True),
        sa.Column("isbn13", sa.VARCHAR(13), nullable=True, unique=True),
        sa.Column("title", sa.Text, nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("authors", sa.ARRAY(sa.Text), nullable=True),
        sa.Column("categories", sa.ARRAY(sa.Text), nullable=True),
        sa.Column("page_count", sa.Integer, nullable=True),
        sa.Column("published_date", sa.Text, nullable=True),
    )


def seed_books_table(table):
    with requests.get(url) as response:
        data = response.json()
    items = data["items"]
    books = []
    for item in items:
        info = item["volumeInfo"]
        identifiers = info.get("industryIdentifiers", [])
        isbn10 = next(
            (isbn["identifier"] for isbn in identifiers if isbn["type"] == "ISBN_10"),
            None,
        )
        isbn13 = next(
            (isbn["identifier"] for isbn in identifiers if isbn["type"] == "ISBN_13"),
            None,
        )
        books.append(
            {
                "isbn10": isbn10,
                "isbn13": isbn13,
                "title": info["title"],
                "description": info.get("description"),
                "authors": info.get("authors"),
                "categories": info.get("categories"),
                "page_count": info.get("pageCount"),
                "published_date": info.get("publishedDate"),
            }
        )
    return op.bulk_insert(table, books)


def upgrade() -> None:
    table = create_books_table()
    seeds = seed_books_table(table)


def downgrade() -> None:
    op.drop_table("books")
