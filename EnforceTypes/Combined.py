from dataclasses import dataclass as dc
from typing import Type, cast

from .types import F, T
from .Classes import classtypes, methtypes

__all__ = [
    "dataclass", "classmeth"
]


def dataclass(cls: Type[T]) -> Type[T]:
    return classtypes(dc(cls))


def classmeth(meth: F) -> F:
    return methtypes(cast(F, classmethod(meth).__func__))
