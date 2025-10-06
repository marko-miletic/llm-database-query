def print_prompt_info() -> None:
    print(
        "Enter your question (press ENTER to just show this prompt again, or type 'quit' to exit):\n"
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
