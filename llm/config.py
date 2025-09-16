from dataclasses import dataclass


@dataclass
class PromptIteration:
    index: int
    prompt: str | None = None
    notes: str | None = None
    sql: str | None = None
