from common import config
from common.constants import DatabaseProvider
from llm.source.config import LLMContext
from llm.source.postgres.introspection import generate_llm_context_data
from functools import lru_cache


DB_PROVIDER_LLM_CONTEXT = {
    DatabaseProvider.POSTGRES.value: generate_llm_context_data,
}


@lru_cache()
def get_context_data() -> LLMContext:
    database_provider = config.DB_PROVIDER
    if database_provider not in DB_PROVIDER_LLM_CONTEXT:
        raise RuntimeError(f"Database provider '{database_provider}' not supported")

    return DB_PROVIDER_LLM_CONTEXT[database_provider]()
