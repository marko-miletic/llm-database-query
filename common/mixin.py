from typing import Iterable


class EnumValuesMixin:
    @classmethod
    def values(cls: Iterable) -> list[str]:
        return [member.value for member in cls]
