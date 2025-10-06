from common.helper import format_query_output
from common.terminal_message import print_prompt_info, print_export_to_file_info
from export.local import export_file
from llm.config import PromptIteration
from llm.run import run


def _print_history(prompts: list[PromptIteration]) -> None:
    if not prompts:
        print("(history is empty)")
        return

    for p in sorted(prompts, key=lambda x: x.index):
        print(f"[{p.index}] {p.prompt}")


def _next_index(prompts: list[PromptIteration]) -> int:
    return (prompts[-1].index + 1) if prompts else 1


def main() -> None:
    prompts = []
    try:
        while True:
            try:
                print_prompt_info()
                user_input = input("> ").strip()
            except EOFError:
                break
            if not user_input:
                continue

            lower = user_input.lower()
            if lower in {"quit", "exit", ":q"}:
                break

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
                print("\nInterrupted. You can type ':help' for commands or 'quit' to exit.")
            except Exception:
                raise

            try:
                print_export_to_file_info()
                file_format = input("> ").strip()
            except EOFError:
                break
            if not file_format:
                continue

            lower = file_format.lower()
            if lower in {"quit", "exit", ":q"}:
                break

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
