from dataclasses import dataclass as dc
from typing import Type

from .Classes import classtypes
from .types import T, cast_to_func

__all__ = [
    "dataclass"
]


def _dataclass(cls: Type[T], **kwargs: bool) -> Type[T]:
    """
    Creates a type-safe dataclass, used just like @dataclasses.dataclass.
    """
    return classtypes(dc(cls, **kwargs))


dataclass = cast_to_func(_dataclass, dc)
dataclass.__doc__ = f"""
Creates a type-safe version of a Dataclass. Used the same as ``@dataclasses.dataclass``

    {dc.__doc__}
"""
print(dataclass.__doc__)
