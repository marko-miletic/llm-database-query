from enum import Enum

from common.mixin import EnumValuesMixin


class DatabaseProvider(str, Enum):
    POSTGRES = "POSTGRES"


class LLMProvider(str, Enum):
    GEMINI = "GEMINI"


class ResponseExportTypes(EnumValuesMixin, str, Enum):
    CSV = "CSV"
    XML = "XML"
    EXCEL = "EXCEL"
    PARQUET = "PARQUET"


class ResponseExportTypesExtensions(EnumValuesMixin, str, Enum):
    CSV = "csv"
    XML = "xml"
    XLSX = "xlsx"
    PARQUET = "parquet"
