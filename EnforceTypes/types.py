from typing import TypeVar, Callable
from typing_extensions import Concatenate, ParamSpec

__all__ = [
    "F", "MISSING", "T"
]


class _MISSING:
    pass


MISSING = _MISSING()
F = TypeVar("F", bound=Callable)
P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")
