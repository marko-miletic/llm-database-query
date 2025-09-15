from llm.source.config import LLMContext

PROMPT_INSTRUCTIONS = """
System / Instruction:
You are a senior test_data analyst generating safe SQL for PostgreSQL 15. Follow the rules:
- Return JSON only with keys: {"sql": string, "notes": string}
- Generate exactly one SELECT statement. 
  No CTEs with writes, no DML/DDL, no temp tables, no functions that modify state.
- Add an explicit LIMIT 100 unless the user specified a lower limit.
- Prefer inner joins only when necessary; avoid Cartesian products.
- Use the provided schema exactly as given. 
  If the question is ambiguous, ask one clarifying question in "notes" and still produce your best safe guess.
- Use ANSI identifiers and correct quoting for strings.
- Do not hallucinate tables or columns.
"""


def get_sql_prompt(user_question: str, llm_context_data: LLMContext) -> str:
    return f"""
        {PROMPT_INSTRUCTIONS}
        Context:
        {llm_context_data.tables_and_columns}
        Relationships:
        {llm_context_data.foreign_keys}
        Rows count:
        {llm_context_data.row_count}
        Sample test_data:
        {llm_context_data.sample_data}
        User question:
        {user_question}
    """
