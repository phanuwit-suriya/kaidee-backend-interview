"""empty message

Revision ID: a3581f615771
Revises: 76996beafe24
Create Date: 2022-02-17 01:20:50.750969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'a3581f615771'
down_revision = '76996beafe24'
branch_labels = None
depends_on = None


def create_histories_table():
    return op.create_table(
        "histories",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("book_id", sa.Integer, sa.ForeignKey("books.id"), nullable=False),
        sa.Column("borrowing_date", sa.DateTime, nullable=False),
        sa.Column("returning_date", sa.DateTime, nullable=True),
    )


def upgrade() -> None:
    create_histories_table()


def downgrade() -> None:
    op.drop_table("histories")
