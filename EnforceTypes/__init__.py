"""
Simple decorator for enforcing types during runtime.

The idea behind this is to reduce time spent developing and using packages
that are computationally intensive and take a long time to run, which might
still fail and error on type problems. The easiest way to resolve this is
checking the types of all input arguments, which quickly becomes repetitive
and does not aid in readability of the code base.

This module provides a simple decorator that handles checking of all input
arguments upon being called, and works for both classes (wrapping __init__)
and it works for singular functions (wrapping any calls made to them).

.. code-block:: python

   from EnforceTypes import enforce_types


   @enforce_types
   def add(a: int, b: int) -> None
       print(f"Adding {a} to {b} equals {a + b}")

   add(2, 2)  # prints "Adding 2 to 2 equals 4"
   add("a", 2)  # This causes the decorator to raise a TypeError!
"""
from typing import Any, Type, TypeVar, get_args

__all__ = [
    "enforce_types"
]


class _MISSING:
    pass


MISSING = _MISSING()
T = TypeVar("T")


def enforce_types(cls: Type[T]) -> Type[T]:
    """A class for use as class decorator. Enforces types in ``init``"""

    def newinit(self: T, *args: Any, **kwargs: Any) -> None:
        keywords = cls.__annotations__ or cls.__init__.__annotations__
        oldinit = self.__dict__.get("__init__") if "__dict__" in dir(self) else None
        oldinit = oldinit or (lambda *a, **k: None)
        arglist = list(args)
        for kw in keywords:
            argval = arglist.pop(0) if len(arglist) > 0 else ...
            kw_val = kwargs.get(kw, MISSING)
            if argval is not ... and kw_val is not MISSING:
                raise TypeError(f"{kw} was given as both a positional and a keyword argument!")
            if kw_val is MISSING:
                if argval is ...:
                    continue
                kw_val = argval
                kwargs[kw] = kw_val
            argtype = keywords[kw]
            argtuple = get_args(argtype)
            if not isinstance(kw_val, argtype) and not isinstance(kw_val, argtuple):
                raise TypeError(f"Argument {kw} was passed a value of type `"
                                f"{type(kw_val).__name__}`, but only accepts values of "
                                f"type `{argtype.__name__}`")
        oldinit(*args, **kwargs)

    setattr(cls, "__init__", newinit)
    return cls
