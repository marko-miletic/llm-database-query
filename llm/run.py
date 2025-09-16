from __future__ import annotations

from common import config
from common.constants import LLMProvider
from db.service import get_query_method_all
from llm.pipelines.text_to_sql import run_text_to_sql
from llm.providers.gemini.client import GeminiClient

DB_PROVIDER_CLIENT = {
    LLMProvider.GEMINI: GeminiClient,
}

def run(user_question: str) -> tuple[str, list[dict], str]:
    llm = DB_PROVIDER_CLIENT[config.LLM_PROVIDER]()
    execute = get_query_method_all()

    return run_text_to_sql(llm, user_question, execute)
