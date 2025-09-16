from common.helper import format_query_output
from llm.config import PromptIteration
from llm.run import run

if __name__ == "__main__":
    prompts = []

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

            prompts.append(
                PromptIteration(
                    index=prompts[-1].index + 1 if prompts else 1,
                    prompt=user_input,
                )
            )
            print(format_query_output(run(prompts)), "\n")

    except KeyboardInterrupt:
        pass
