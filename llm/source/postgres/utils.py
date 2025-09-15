from pathlib import Path
from typing import Iterable

from db.providers.postgres.client import PostgreSQLClient

SQL_DIR = Path(__file__).parent / "sql"


def read_sql(name: str) -> str:
    path = SQL_DIR / name

    return path.read_text(encoding="utf-8")


def rows_to_string(rows: Iterable[dict]) -> str:
    result: list[str] = []
    for row in rows:
        if not isinstance(row, dict):
            result.append(str(row))
            continue

        parts = [f"{k}={row[k]}" for k in row.keys()]
        result.append(", ".join(parts))

    return "\n".join(result)


def get_context_string(sql: str | None = None, sql_file_name: str | None = None) -> str:
    if sql is None and sql_file_name is None:
        raise ValueError("Either sql or sql_file_name must be specified")

    sql_string = sql or read_sql(sql_file_name)
    query_rows = PostgreSQLClient().all(sql_string)

    return rows_to_string(query_rows)
