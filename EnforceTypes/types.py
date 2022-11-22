from typing import TypeVar, Callable, cast
from typing_extensions import ParamSpec

__all__ = [
    "F", "MISSING", "T"
]


class _MISSING:
    pass


MISSING = _MISSING()
F = TypeVar("F", bound=Callable)
F2 = TypeVar("F2", bound=Callable)
P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")


def cast_to_func(fn: F2, target: F) -> F:
    """
    Casts function ``fn`` to ``target`` to aid with autocomplete and whatnot.
    """
    return cast(F, fn)
