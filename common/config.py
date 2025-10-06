from os import getenv

from dotenv import load_dotenv

from common.constants import DatabaseProvider, LLMProvider

load_dotenv()

DB_PROVIDER = DatabaseProvider(getenv("DB_PROVIDER", DatabaseProvider.POSTGRES.value))
LLM_PROVIDER = LLMProvider(getenv("LLM_PROVIDER", LLMProvider.GEMINI.value))

DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")

GEMINI_API_KEY = getenv("GEMINI_API_KEY")
GEMINI_MODEL = "models/gemini-2.5-pro"

SAMPLE_DATA_LIMIT = 10

TERMINAL_OUTPUT_COLUMN_WIDTH = 40

EXPORT_FILE_BASE_NAME = "query_export"
