from llm.source.config import LLMContext

PROMPT_INSTRUCTIONS = """
System / Instruction:
You are a senior data analyst generating safe SQL for PostgreSQL 15. Follow the rules:
- Return JSON only with keys: {"tables": list[string]}
- Use the provided schema exactly as given.
- Use ANSI identifiers and correct quoting for strings.
- Do not hallucinate tables or columns.
"""

PROMPT = """
Question:
For the provided context, extract all the required table names that are used.
"""


def get_sample_data_prompt(user_question: str, llm_context_data: LLMContext) -> str:
    return f"""
        {PROMPT_INSTRUCTIONS}
        Context:
        {llm_context_data.tables_and_columns}
        Relationships:
        {llm_context_data.foreign_keys}
        Rows count:
        {llm_context_data.row_count}
        User question:
        {user_question}
        Prompt:
        {PROMPT}
    """
