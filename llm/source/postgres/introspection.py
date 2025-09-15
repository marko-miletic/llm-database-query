from llm.source.config import LLMContext
from llm.source.postgres.utils import get_context_string


def _row_count() -> str:
    return get_context_string(sql_file_name="row_count.sql")


def _tables_and_columns() -> str:
    return get_context_string(sql_file_name="tables_and_columns.sql")


def _foreign_keys() -> str:
    return get_context_string(sql_file_name="foreign_keys.sql")


def generate_llm_context_data() -> LLMContext:
    return LLMContext(
        row_count=_row_count(),
        foreign_keys=_foreign_keys(),
        tables_and_columns=_tables_and_columns(),
    )
