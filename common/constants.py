from enum import Enum


class DatabaseProvider(str, Enum):
    POSTGRES = "POSTGRES"


class LLMProvider(str, Enum):
    GEMINI = "GEMINI"


class ResponseExportTypes(str, Enum):
    CSV = "CSV"
    XML = "XML"
    EXCEL = "EXCEL"
    PARQUET = "PARQUET"
