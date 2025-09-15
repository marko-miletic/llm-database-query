from typing import Protocol


class DatabaseClient(Protocol):
    def one(self, sql: str) -> dict | None:
        raise NotImplemented

    def all(self, sql: str) -> list[dict]:
        raise NotImplemented
