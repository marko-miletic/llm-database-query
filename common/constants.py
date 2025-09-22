from enum import Enum


class DatabaseProvider(str, Enum):
    POSTGRES = "POSTGRES"


class LLMProvider(str, Enum):
    GEMINI = "GEMINI"
