from dataclasses import dataclass as dc
from typing import Type, cast

from .types import F, T
from .Classes import classtypes, methtypes
from.Functions import functypes

__all__ = [
    "dataclass"
]


def dataclass(cls: Type[T]) -> Type[T]:
    return classtypes(dc(cls))


def staticmeth(meth: F) -> F:
    return cast(F, staticmethod(functypes(meth)))
