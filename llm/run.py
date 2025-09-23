from common import config
from common.constants import LLMProvider
from db.service import get_query_method_all
from llm.config import PromptIteration
from llm.pipelines.text_to_sql import run_text_to_sql
from llm.providers.gemini.client import GeminiClient

LLM_PROVIDER_CLIENT = {
    LLMProvider.GEMINI.value: GeminiClient,
}


def run(prompts: list[PromptIteration]) -> list[PromptIteration]:
    llm = LLM_PROVIDER_CLIENT[config.LLM_PROVIDER]()
    execute = get_query_method_all()

    return run_text_to_sql(llm, prompts, execute)
