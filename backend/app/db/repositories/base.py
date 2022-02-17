from typing import NoReturn

from databases import Database


class BaseRepository:
    def __init__(self, db: Database) -> NoReturn:
        self.db = db
