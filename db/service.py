from typing import Callable

from common import config
from common.constants import DatabaseProvider
from common.error import DatabaseError
from db.core.client import DatabaseClient
from db.providers.postgres.client import PostgreSQLClient

DB_PROVIDER_CLIENT = {
    DatabaseProvider.POSTGRES.value: PostgreSQLClient,
}


def get_db_client() -> DatabaseClient:
    database_provider = config.DB_PROVIDER

    if database_provider not in DB_PROVIDER_CLIENT:
        raise DatabaseError(f"Database provider '{database_provider}' not supported")

    return DB_PROVIDER_CLIENT[database_provider]()


def get_query_method_all() -> Callable[[str], list[dict]]:
    return get_db_client().all
