from dataclasses import dataclass as dc
from typing import Type

from .types import T
from .Classes import classtypes

__all__ = [
    "dataclass"
]


def dataclass(cls: Type[T]) -> Type[T]:
    return classtypes(dc(cls))
