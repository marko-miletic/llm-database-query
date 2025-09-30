from enum import Enum


class DatabaseProvider(str, Enum):
    POSTGRES = "POSTGRES"


class LLMProvider(str, Enum):
    GEMINI = "GEMINI"


class ResponseExportTypes(str, Enum):
    TXT = "TXT"
    CSV = "CSV"
    XML = "XML"
    EXCEL = "EXCEL"
    PARQUET = "PARQUET"


class ResponseExportTypesExtensions(str, Enum):
    TXT = "txt"
    CSV = "csv"
    XML = "xml"
    XLSX = "xlsx"
    PARQUET = "parquet"
