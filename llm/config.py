from dataclasses import dataclass


@dataclass
class PromptIteration:
    index: int
    response: list[dict] | None = None
    prompt: str | None = None
    notes: str | None = None
    sql: str | None = None
