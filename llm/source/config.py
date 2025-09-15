from dataclasses import dataclass


@dataclass
class LLMContext:
    row_count: str
    foreign_keys: str
    tables_and_columns: str
    sample_data: str | None = None
