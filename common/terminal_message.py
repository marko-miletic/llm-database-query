from llm.config import PromptIteration


def print_prompt_info() -> None:
    print(
        "Enter your question (press ENTER to just show this prompt again, or type 'quit' to exit):\n"
        "  :export    Export response data to local file\n"
        "  :history   Show prompt history indexes and questions\n"
        "  :reset     Clear prompt history\n"
        "  quit/exit  Exit the program\n"
    )


def print_export_to_file_info() -> None:
    print(
        "Choose the file format (press ENTER to skip file export):\n"
        "  (*) CSV\n"
        "  (*) XML\n"
        "  (*) EXCEL\n"
        "  (*) PARQUET\n"
        "  quit/exit  Exit the program\n"
    )


def print_history(prompts: list[PromptIteration]) -> None:
    if not prompts:
        print("(history is empty)\n")
        return

    for p in sorted(prompts, key=lambda x: x.index):
        print(f"[{p.index}] {p.prompt}")

    print()
