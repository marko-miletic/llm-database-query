from contextlib import contextmanager
from typing import Iterator

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool

from common import config
from common.error import PostgreSQLDatabaseError
from db.config import Credentials


class Database:
    _pool: SimpleConnectionPool | None = None

    @classmethod
    def _initialize_pool(cls) -> None:
        if cls._pool is None:
            credentials = Credentials(
                db_host=config.DB_HOST,
                db_port=config.DB_PORT,
                db_name=config.DB_NAME,
                db_user=config.DB_USER,
                db_password=config.DB_PASSWORD,
            )
            cls._pool = SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dbname=credentials.db_name,
                user=credentials.db_user,
                password=credentials.db_password,
                host=credentials.db_host,
                port=credentials.db_port,
            )

    @classmethod
    @contextmanager
    def get_cursor(cls, dict_cursor: bool = True) -> Iterator[RealDictCursor | psycopg2.extensions.cursor]:
        cls._initialize_pool()
        if cls._pool is None:
            raise PostgreSQLDatabaseError("Database connection pool is not initialized.")

        connection = cls._pool.getconn()
        try:
            with connection, connection.cursor(cursor_factory=RealDictCursor if dict_cursor else None) as cursor:
                yield cursor
        finally:
            cls._pool.putconn(connection)
