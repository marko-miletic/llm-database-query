from common.helper import format_query_output
from common.terminal_message import print_prompt_info, print_export_to_file_info, print_history
from export.local import export_file
from llm.config import PromptIteration
from llm.run import run


def main() -> None:
    prompts = []
    try:
        while True:
            try:
                print_prompt_info()
                user_input = input("(>) ").strip()
            except EOFError:
                break
            if not user_input:
                continue

            lower = user_input.lower()
            if lower in {"quit", "exit", ":q"}:
                break

            if lower == ":history":
                print_history(prompts)
                continue

            if lower == ":reset":
                prompts.clear()
                print("(History cleared.)\n")
                continue

            if lower == ":export":
                if not prompts:
                    print("(No data available for export.)\n")
                    continue

                try:
                    print_export_to_file_info()
                    file_format = input("(>) ").strip()
                except EOFError:
                    break
                if not file_format:
                    continue

                lower = file_format.lower()
                if lower in {"quit", "exit", ":q"}:
                    break

                try:
                    full_path = export_file(file_format, prompts[-1].response)
                    print(f"\n(File exported successfully at {full_path}.)\n")
                except ValueError as e:
                    print(e)
                    break

                continue

            prompts.append(
                PromptIteration(
                    index=(prompts[-1].index + 1) if prompts else 1,
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

    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    raise SystemExit(main())
