from dataclasses import dataclass


@dataclass
class DatabaseProvider:
    POSTGRES = "POSTGRES"


@dataclass
class LLMProvider:
    GEMINI = "GEMINI"
