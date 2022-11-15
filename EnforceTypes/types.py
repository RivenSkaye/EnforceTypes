from typing import TypeVar, Callable

__all__ = [
    "F", "MISSING", "T"
]


class _MISSING:
    pass


MISSING = _MISSING()
T = TypeVar("T")
F = TypeVar("F", bound=Callable)
