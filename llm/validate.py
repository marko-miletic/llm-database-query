import re

from llm.config import PromptIteration

MODIFICATION_KEYWORDS = {
    "insert",
    "update",
    "delete",
    "merge",
    "upsert",
    "replace",
    "create",
    "alter",
    "drop",
    "truncate",
    "rename",
    "reindex",
    "begin",
    "commit",
    "rollback",
    "savepoint",
    "release",
    "grant",
    "revoke",
    "set",
    "show",
    "use",
    "analyze",
    "vacuum",
    "pragma",
    "call",
    "do",
    "exec",
    "execute",
    "prepare",
    "deallocate",
    "explain",
    "copy",
    "load",
    "import",
    "export",
}

RE_CTE_START = re.compile(r"^\s*\(?\s*with\b", re.IGNORECASE)
RE_SELECT_START = re.compile(r"^\s*\(?\s*select\b", re.IGNORECASE)
RE_EXPLAIN_START = re.compile(r"^\s*\(?\s*explain\b", re.IGNORECASE)
RE_WORD_BOUNDARY = {
    kw: re.compile(r"\b{re.escape(kw)}\b", re.IGNORECASE)
    for kw in MODIFICATION_KEYWORDS
}
RE_SELECT_INTO = re.compile(r"\bselect\b[^;]*\binto\b", re.IGNORECASE | re.DOTALL)


def _ensure_single_statement(sql: str) -> None:
    semicolons = [m.start() for m in re.finditer(r";", sql)]
    if not semicolons:
        return

    last = semicolons[-1]
    tail = sql[last + 1 :].strip()
    if len(semicolons) > 1 or tail:
        raise ValueError("Only a single SELECT statement is allowed.")


def _disallow_cte(sql: str) -> None:
    if RE_CTE_START.search(sql):
        raise ValueError(
            f"CTEs are not allowed (queries starting with WITH are rejected)."
        )


def _disallow_modifications(sql: str) -> None:
    for kw, pat in RE_WORD_BOUNDARY.items():
        if pat.search(sql):
            raise ValueError(f"Disallowed statement/keyword detected: {kw.upper()}.")


def _require_select_start(sql: str) -> None:
    if RE_EXPLAIN_START.search(sql):
        raise ValueError("Only SELECT statements are allowed (no EXPLAIN).")
    if not RE_SELECT_START.search(sql):
        raise ValueError("Only SELECT statements are allowed.")


def _disallow_select_into(sql: str) -> None:
    if RE_SELECT_INTO.search(sql):
        raise ValueError("SELECT ... INTO is not allowed.")


def validate(iteration_instance: PromptIteration) -> None:
    if not iteration_instance.sql.strip():
        raise ValueError(f"SQL prompt must be a non-empty string. Notes {iteration_instance.notes}.")

    _ensure_single_statement(iteration_instance.sql)
    _disallow_cte(iteration_instance.sql)
    _require_select_start(iteration_instance.sql)

    _disallow_modifications(iteration_instance.sql)
    _disallow_select_into(iteration_instance.sql)
