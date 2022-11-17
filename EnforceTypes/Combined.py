from dataclasses import dataclass as dc
from typing import Type

from .Classes import classtypes
from .types import T

__all__ = [
    "dataclass"
]


def dataclass(cls: Type[T]) -> Type[T]:
    return classtypes(dc(cls))
