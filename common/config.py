from os import getenv

from dotenv import load_dotenv

load_dotenv()

DB_PROVIDER = getenv("DB_PROVIDER")
LLM_PROVIDER = getenv("LLM_PROVIDER")

DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")

GEMINI_API_KEY = getenv("GEMINI_API_KEY")
GEMINI_MODEL = "models/gemini-2.5-flash"

SAMPLE_DATA_LIMIT = 10

TERMINAL_OUTPUT_COLUMN_WIDTH = 40
