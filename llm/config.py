from dataclasses import dataclass
from typing import Any


@dataclass
class PromptIteration:
    index: int
    response: list[dict[str, Any]] | None = None
    prompt: str | None = None
    notes: str | None = None
    sql: str | None = None
