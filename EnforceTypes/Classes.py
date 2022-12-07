"""
A series of decorators for use with and in *classes* only.
These functions are meant to provide both EnforceTypes wrapping, as well as making
sure that the handling order for common combined decorators is safely handled.
Reduces combined decorators down to one by applying decorators like ``@dataclass``
and ``@staticmethod`` in the right order.
"""

from functools import wraps
from inspect import _ParameterKind as PK
from inspect import signature
from types import FunctionType
from typing import Any, Callable, Iterable, Type, cast
from typing_extensions import get_args

from .types import MISSING, F, T
from .utils import resolve_types


def classtypes(cls: Type[T]) -> Type[T]:
    """For use as class decorator. Enforces types in ``init``"""
    oldinit: Callable = getattr(cls, "__init__")
    # If this constructor is a built-in object or otherwise a wrapper around something
    # then instantiation behavior is different
    is_obj = not isinstance(oldinit, FunctionType)
    keywords = signature(cls).parameters

    def newinit(self: Type[T], *args: Any, **kwargs: Any) -> None:
        arglist = list(args)
        for kw in keywords:
            argval = arglist.pop(0) if len(arglist) > 0 else ...
            kw_val = kwargs.get(kw, MISSING)
            if argval is not ... and kw_val is not MISSING:
                raise TypeError(f"{kw} was given as both a positional and a keyword argument! "
                                f"({cls.__name__})")
            if kw_val is MISSING:
                if argval is ...:
                    continue
                kw_val = argval
                if keywords[kw].kind == PK.POSITIONAL_ONLY:
                    arglist.append(kw_val)
                else:
                    if keywords[kw].kind == PK.KEYWORD_ONLY and kw not in kwargs:
                        raise SyntaxError(f"{kw} is a keyword-only argument, but was given as "
                                          f"positional argument! ({cls.__name__})")
                    kwargs[kw] = kw_val
            argtype = resolve_types(keywords[kw].annotation)
            argtuple = tuple(resolve_types(_t) for _t in get_args(argtype))
            typecheck = isinstance(kw_val, argtype)
            tuplecheck = True if len(argtuple) == 0 else isinstance(kw_val, argtuple)
            if not typecheck or not tuplecheck:
                argnames = ", "
                if isinstance(argtype, Iterable):
                    argnames = argnames.join([a.__name__ for a in argtype])
                else:
                    argnames = argtype.__name__
                raise TypeError(f"Argument {kw} was passed a value of type `"
                                f"{type(kw_val).__name__}`, but only accepts values of "
                                f"type(s) `{argnames}` "
                                f"({cls.__name__})")
        if is_obj:
            oldinit(self)
        else:
            oldinit(self, **kwargs)

    setattr(cls, "__init__", newinit)
    return cls


def methtypes(meth: F) -> F:
    """For use as a decorator for methods and @classmethods where ``self`` or ``cls`` is passed"""
    assert meth

    @wraps(meth)
    def newcall(selfcls: Type[T], *args: Any, **kwargs: Any) -> Any:
        keywords = signature(meth).parameters
        arglist = list(args)
        for kw in keywords:
            if kw in ["self", "cls"]:
                continue
            argval = arglist.pop(0) if len(arglist) > 0 else ...
            kw_val = kwargs.get(kw, MISSING)
            if argval is not ... and kw_val is not MISSING:
                raise SyntaxError(f"{kw} was given as both a positional and a keyword argument! "
                                  f"({meth.__name__})")
            if kw_val is MISSING:
                if argval is ...:
                    continue
                kw_val = argval
                if keywords[kw].kind == PK.POSITIONAL_ONLY:
                    arglist.append(kw_val)
                else:
                    if keywords[kw].kind == PK.KEYWORD_ONLY and kw not in kwargs:
                        raise SyntaxError(f"{kw} is a keyword-only argument, but was given as "
                                          f"positional argument! ({meth.__name__})")
                    kwargs[kw] = kw_val
            argtype = resolve_types(keywords[kw].annotation)
            argtuple = tuple(resolve_types(_t) for _t in get_args(argtype))
            typecheck = isinstance(kw_val, argtype)
            tuplecheck = True if len(argtuple) == 0 else isinstance(kw_val, argtuple)
            if not typecheck or not tuplecheck:
                argnames = ", "
                if isinstance(argtype, Iterable):
                    argnames = argnames.join([a.__name__ for a in argtype])
                else:
                    argnames = argtype.__name__
                raise TypeError(f"Argument {kw} was passed a value of type `"
                                f"{type(kw_val).__name__}`, but only accepts values of "
                                f"type(s) `{argnames}` "
                                f"({meth.__name__})")
        return meth(selfcls, *arglist, **kwargs)

    return cast(F, newcall)
