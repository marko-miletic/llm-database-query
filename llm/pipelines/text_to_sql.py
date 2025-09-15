from __future__ import annotations

import json
import re
from typing import Callable

from llm.core.client import LLMClient
from llm.prompt.context import get_context_data
from llm.prompt.generate_sql_prompt import get_sql_prompt
from llm.sample.generate_sample_data_prompt import get_sample_data_prompt
from llm.source.postgres.sample import get_tables_sample_data
from llm.validate import validate

RE_CODE_FENCE = re.compile(r"^```(json)?|```$", flags=re.M)


def _extract_response_data(raw_text: str) -> dict:
    if raw_text is None:
        raise ValueError("Model returned empty response.")

    text = raw_text.strip()
    text = RE_CODE_FENCE.sub("", text.strip())

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse model JSON: {e}\nRaw text: {raw_text}"
        ) from e


def _generate_sample_data_tables(
    llm: LLMClient, user_question: str, context_data
) -> list[str] | None:
    prompt = get_sample_data_prompt(user_question, context_data)
    prompt_response = llm.generate(prompt)
    data = _extract_response_data(prompt_response)

    tables = data.get("tables")
    if tables is None or not isinstance(tables, list):
        return []

    return tables


def run_text_to_sql(
    llm: LLMClient, user_question: str, execute_sql: Callable[[str], list[dict]]
) -> tuple[list[dict], str]:
    context_data = get_context_data()

    sample_tables = _generate_sample_data_tables(llm, user_question, context_data)
    if sample_tables:
        context_data.sample_data = get_tables_sample_data(sample_tables)

    sql_prompt = get_sql_prompt(user_question, context_data)
    sql_raw = llm.generate(sql_prompt)
    sql_payload = _extract_response_data(sql_raw)

    sql = sql_payload.get("sql")
    notes = sql_payload.get("notes", "")

    validate(sql, notes)

    return execute_sql(sql), notes
