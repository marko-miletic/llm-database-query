from common.error import FileExportError
from common.helper import format_query_output
from common.terminal_message import print_prompt_info, print_export_to_file_info, print_history
from export.local import export_file
from llm.config import PromptIteration
from llm.run import run


class ChatTerminal:
    def __init__(self) -> None:
        self._prompts = []
        self._running = True
        self._commands = {
            ":history": self._handle_history,
            ":export": self._handle_export,
            ":reset": self._handle_reset,
            # exit commands
            ":quit": self._handle_quit,
            ":exit": self._handle_quit,
            ":q": self._handle_quit,
        }

    def run(self) -> None:
        while self._running:
            try:
                print_prompt_info()
                user_input = input("(>) ").strip()
                if not user_input:
                    continue

                if user_input.lower() not in self._commands:
                    if user_input.startswith(":"):
                        print("(Invalid command input!)\n")
                        continue

                    self._handle_prompt(user_input)
                else:
                    self._commands[user_input.lower()]()

            except (KeyboardInterrupt, EOFError):
                self._running = False

    def _handle_prompt(self, prompt_text: str) -> None:
        self._prompts.append(
            PromptIteration(index=(self._prompts[-1].index + 1) if self._prompts else 1, prompt=prompt_text)
        )

        try:
            result = run(self._prompts)
            print(format_query_output(result), "\n")
        except Exception as e:
            print(f"An error occurred: {e}")
            self._prompts.pop()

    def _handle_history(self) -> None:
        print_history(self._prompts)

    def _handle_reset(self) -> None:
        self._prompts.clear()
        print("(History cleared.)\n")

    def _handle_quit(self) -> None:
        self._running = False
        print("(Goodbye!)")

    def _handle_export(self) -> None:
        if not self._prompts:
            print("(No data available for export.)\n")
            return

        print_export_to_file_info()
        file_format = input("(format>) ").strip()

        if not file_format or file_format.lower() in {"quit", "exit", ":q"}:
            print("(Export cancelled.)\n")
            return

        try:
            last_response = self._prompts[-1].response
            full_path = export_file(file_format, last_response)
            print(f"(File exported successfully at {full_path}.)\n")
        except FileExportError as e:
            print(f"Export Error: {e}")
