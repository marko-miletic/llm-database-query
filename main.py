import sys

from common.helper import format_query_output
from llm.run import run

DEFAULT_PROMPT = "Give me some random data from the database!"


def _execute_and_print(prompt: str) -> None:
    print("Prompt:", prompt, "\n")
    print(format_query_output(run(prompt)), "\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        first_prompt = sys.argv[1]
        _execute_and_print(first_prompt)
    else:
        _execute_and_print(DEFAULT_PROMPT)

    try:
        while True:
            try:
                user_input = input(
                    "Enter your next question (press ENTER to just show this prompt again, or type 'quit' to exit):\n> "
                ).strip()
            except EOFError:
                break
            if not user_input:
                continue
            if user_input.lower() in {"quit", "exit", ":q"}:
                break

            _execute_and_print(user_input)

    except KeyboardInterrupt:
        pass
