import sys

from common.helper import format_query_output
from llm.run import run

DEFAULT_PROMPT = (
    "Give me some random data from the database!"
)

if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PROMPT
    print(format_query_output(run(prompt)))
