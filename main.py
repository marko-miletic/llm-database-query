from common.export import export_file
from common.helper import format_query_output
from llm.config import PromptIteration
from llm.run import run


def _print_help() -> None:
    print(
        "Commands:\n"
        "  :help      Show this help\n"
        "  :history   Show prompt history indexes and questions\n"
        "  :reset     Clear prompt history\n"
        "  quit/exit  Exit the program\n"
    )


def _print_history(prompts: list[PromptIteration]) -> None:
    if not prompts:
        print("(history is empty)")
        return

    for p in sorted(prompts, key=lambda x: x.index):
        print(f"[{p.index}] {p.prompt}")


def _next_index(prompts: list[PromptIteration]) -> int:
    return (prompts[-1].index + 1) if prompts else 1


def main() -> None:
    prompt_text = "Enter your next question (press ENTER to just show this prompt again, or type 'quit' to exit):\n> "
    export_text = "Choose the file format:\n> "

    prompts = []
    try:
        while True:
            try:
                user_input = input(prompt_text).strip()
            except EOFError:
                break
            if not user_input:
                continue

            lower = user_input.lower()
            if lower in {"quit", "exit", ":q"}:
                break

            if lower == ":help":
                _print_help()
                continue
            if lower == ":history":
                _print_history(prompts)
                continue
            if lower == ":reset":
                prompts.clear()
                print("History cleared.")
                continue

            prompts.append(
                PromptIteration(
                    index=_next_index(prompts),
                    prompt=user_input,
                )
            )

            try:
                result = run(prompts)
                print(format_query_output(result), "\n")
            except KeyboardInterrupt:
                print(
                    "\nInterrupted. You can type ':help' for commands or 'quit' to exit."
                )
            except Exception:
                raise

            try:
                file_format = input(export_text).strip()
            except EOFError:
                break
            if not file_format:
                continue

            try:
                full_path = export_file(file_format, prompts[-1].response)
                print(f"\nFile exported successfully at {full_path}.")
            except ValueError as e:
                print(e)
                break

    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    raise SystemExit(main())
