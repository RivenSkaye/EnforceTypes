"""
Simple decorator for enforcing types during runtime.

The idea behind this is to reduce time spent developing and using packages
that are computationally intensive and take a long time to run, which might
still fail and error on type problems. The easiest way to resolve this is
checking the types of all input arguments, which quickly becomes repetitive
and does not aid in readability of the code base.

This module provides simple decorators that handle checking of all input
arguments upon being called, for both classes (wrapping __init__)
and singular functions (wrapping any calls made to them).

.. code-block:: python

   from EnforceTypes import classtypes, functypes


   @functypes
   def add(a: int, b: int) -> None
       print(f"Adding {a} to {b} equals {a + b}")


   add(2, 2)  # prints "Adding 2 to 2 equals 4"
   add("a", 2)  # This causes the decorator to raise a TypeError!

   @classtypes
   class A:
       def __init__(a: int, b: int):
           self.a = a
           self.b = b

       @property
       calc():
           print(f"Adding {self.a} to {self.b} equals {self.a + self.b}")


    A(1, 1).calc  # prints 2
    A(1, "b").calc  # This causes a TypeError too, before calling `A.calc`!
"""
from typing import Any, Type, TypeVar, get_args, Callable, Dict
from functools import wraps

__all__ = [
    "classtypes", "functypes"
]

__version__ = "0.0.1"


class _MISSING:
    pass


MISSING = _MISSING()
T = TypeVar("T")
classtype = type(_MISSING)


def classtypes(cls: Type[T]) -> Type[T]:
    """For use as class decorator. Enforces types in ``init``"""

    @wraps(cls)
    def newinit(self: Type[T], *args: Any, **kwargs: Any) -> None:
        keywords: Dict[str, Any] = self.dict.get("__init__").__annotations__  # type: ignore
        oldinit: Callable = self.__dict__.get("__init__")  # type: ignore
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
        oldinit(*arglist, **kwargs)

    setattr(cls, "__init__", newinit)
    return cls


def functypes(func: Callable) -> Callable:
    """For use as a function decorator, enforces types in ``__call__``"""

    @wraps(func)
    def newcall(func: Callable, *args: Any, **kwargs: Any) -> T:
        keywords = func.__annotations__
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
        return func(*arglist, **kwargs)

    return newcall
