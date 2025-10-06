import json

from common.helper import custom_json_serial
from llm.config import PromptIteration
from llm.source.config import LLMContext

PROMPT_INSTRUCTIONS = """
## Persona & Goal
You are a world-class, senior database data analyst. 
Your primary goal is to convert a user's natural language question 
into a single, safe, and syntactically correct database SELECT statement.

## Output Requirements
You **MUST** respond with a single, raw JSON object (no markdown, no preamble).
The JSON object must have exactly two keys:
- `sql`: A string containing the generated SQL query.
- `notes`: A string explaining your step-by-step reasoning for building the query. 
    This must include which tables and columns you chose, how you decided to join them, and any assumptions you made. 
    If the user's question is ambiguous, state your best guess and ask a single clarifying question here.

Example format:
```json
{
  "sql": "SELECT ...",
  "notes": "Step 1: Identified the need for columns X and Y from the user's question.\\n
  Step 2: Located column X in `table_a` and column Y in `table_b`.\\n
  Step 3: Used the foreign key `table_a.id -> table_b.a_id` to perform a LEFT JOIN.\\n
  Step 4: Added a LIMIT of 100 as no other limit was specified."
}
"""


def _format_prompt_history(prompts: list[PromptIteration]) -> str:
    if not prompts:
        return "No previous prompts / history."

    output = []
    for p in sorted(prompts, key=lambda x: x.index)[:-1]:
        output.append(
            {
                "turn": p.index,
                "user_question": p.prompt,
                "your_notes": p.notes,
                "generated_sql": p.sql,
                "query_result_preview": p.response[:5] if p.response else None,
            }
        )

    return json.dumps(output, indent=2, default=custom_json_serial)


def get_sql_prompt(prompts: list[PromptIteration], context_data: LLMContext) -> str:
    current_question = prompts[-1].prompt

    return f"""
{PROMPT_INSTRUCTIONS}

## Prompt History
{_format_prompt_history(prompts)}

## Database Schema
### Tables & Columns
{context_data.tables_and_columns}

### Relationships (Foreign Keys)
{context_data.foreign_keys}

### Table Row Counts
{context_data.row_count}

### Sample Data
{context_data.sample_data}

## User Question
{current_question}
"""
