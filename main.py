from app.terminal.command import CommandTerminal


def main() -> None:
    app = CommandTerminal()
    app.run()


if __name__ == "__main__":
    raise SystemExit(main())
