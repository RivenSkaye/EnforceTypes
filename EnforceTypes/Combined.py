from dataclasses import dataclass as dc
from functools import partial
from typing import Callable, Optional, Type, cast

from .Classes import classtypes
from .types import T, cast_to_func

__all__ = [
    "dataclass"
]


def _dataclass(cls: Optional[Type[T]] = None, **kwargs: bool) -> Callable[[Type[T]], Type[T]]:
    """
    Creates a type-safe dataclass, used just like @dataclasses.dataclass.
    """
    if cls is not None:
        cls = cast(Type, cls)
        return classtypes(dc(cls, **kwargs))
    else:
        return cast(Callable, partial(_dataclass, **kwargs))


dataclass = cast_to_func(_dataclass, dc)
