from typing import Any, Dict, List, Optional, Tuple

from db.core.client import DatabaseClient
from db.providers.postgres.connection import Database


class PostgreSQLClient(DatabaseClient):
    def one(self, sql: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[Dict[str, Any]]:
        with Database.get_cursor() as cursor:
            cursor.execute(sql, params)
            if cursor.description is None:
                return None

            return cursor.fetchone()

    def all(self, sql: str, params: Optional[Tuple[Any, ...]] = None) -> List[Dict[str, Any]]:
        with Database.get_cursor() as cur:
            cur.execute(sql, params)
            if cur.description is None:
                return []

            return cur.fetchall()
