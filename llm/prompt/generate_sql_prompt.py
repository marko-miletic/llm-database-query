from llm.config import PromptIteration
from llm.source.config import LLMContext

PROMPT_INSTRUCTIONS = """
System / Instruction:
You are a senior data analyst generating safe SQL for PostgreSQL 15. Follow the rules:
- Return JSON only with keys: {"sql": string, "notes": string}
- Generate exactly one SELECT statement. 
  No CTEs with writes, no DML/DDL, no temp tables, no functions that modify state.
- Add an explicit LIMIT 100 unless the user specified a lower limit.
- Prefer inner joins only when necessary; avoid Cartesian products.
- Use the provided schema exactly as given. 
  If the question is ambiguous, ask one clarifying question in "notes" and still produce your best safe guess.
- Use ANSI identifiers and correct quoting for strings.
- Do not hallucinate tables or columns.
- Prompt history is ordered by index value for each history instance
- Rely heavily on the prompt history if possible and do not ignore it in any way.
"""


def _format_prompt_history(prompts: list[PromptIteration]) -> list[dict]:
    output = []
    for p in sorted(prompts, key=lambda x: x.index)[:-1]:
        output.append(
            {
                "index": p.index,
                "prompt": p.prompt,
                "notes": p.notes,
                "sql": p.sql,
                "response": p.response[:5] if p.response else None,
            }
        )

    return output


def get_sql_prompt(prompts: list[PromptIteration], context_data: LLMContext) -> str:
    return f"""
        {PROMPT_INSTRUCTIONS} \n
        Prompt history:
        {_format_prompt_history(prompts)} \n
        Context:
        {context_data.tables_and_columns} \n
        Relationships:
        {context_data.foreign_keys} \n
        Rows count:
        {context_data.row_count} \n
        Sample data:
        {context_data.sample_data} \n
        User question:
        {prompts[-1].prompt} \n
    """
