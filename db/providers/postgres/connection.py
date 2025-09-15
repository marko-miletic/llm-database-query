from contextlib import contextmanager
from typing import Generator

import psycopg2
import psycopg2.extras

from common import config
from db.config import Credentials


def _credentials() -> Credentials:
    credentials = Credentials(
        db_host=config.DB_HOST,
        db_port=config.DB_PORT,
        db_name=config.DB_NAME,
        db_user=config.DB_USER,
        db_password=config.DB_PASSWORD,
    )

    return credentials


def _connect(credentials: Credentials) -> psycopg2._psycopg.connection:
    return psycopg2.connect(
        dbname=credentials.db_name,
        user=credentials.db_user,
        password=credentials.db_password,
        host=credentials.db_host,
        port=credentials.db_port,
    )


@contextmanager
def get_cursor(
    dict_rows: bool = True,
) -> Generator[psycopg2._psycopg.cursor, None, None]:
    connection = None
    cursor = None

    try:
        credentials = _credentials()
        connection = _connect(credentials)
        if not dict_rows:
            cursor = connection.cursor()
        else:
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        yield cursor
        connection.commit()

    except Exception:
        if connection is not None:
            connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
