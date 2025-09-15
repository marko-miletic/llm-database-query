from common import config
from llm.source.postgres.utils import get_context_string


def get_tables_sample_data(tables: list[str]) -> str:
    data_samples = {}

    for t in tables:
        sql_string = f"SELECT * FROM {t} LIMIT {config.SAMPLE_DATA_LIMIT};"
        data_samples[t] = get_context_string(sql=sql_string)

    return "\n".join(f"table:{k}\n{v}" for k, v in data_samples.items())
