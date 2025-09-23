from db.core.client import DatabaseClient
from db.providers.postgres.connection import get_cursor


class PostgreSQLClient(DatabaseClient):
    def __init__(self) -> None:
        self._cursor = get_cursor

    def one(self, sql: str) -> dict | None:
        with self._cursor() as cursor:
            cursor.execute(sql)
            if cursor.description is None:
                return None

            return cursor.fetchone()

    def all(self, sql: str) -> list[dict]:
        with self._cursor() as cur:
            cur.execute(sql)
            if cur.description is None:
                return []

            return cur.fetchall()
