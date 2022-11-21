from functools import wraps
from inspect import _ParameterKind as PK
from inspect import signature
from typing import Any, cast
from typing_extensions import get_args

from .types import MISSING, F


__all__ = [
    "functypes"
]


def functypes(func: F) -> F:
    """For use as a function decorator, enforces types in ``__call__``"""
    assert func

    @wraps(func)
    def newcall(*args: Any, **kwargs: Any) -> Any:
        keywords = signature(func).parameters
        arglist = list(args)
        for kw in keywords:
            argval = arglist.pop(0) if len(arglist) > 0 else ...
            kw_val = kwargs.get(kw, MISSING)
            if argval is not ... and kw_val is not MISSING:
                raise SyntaxError(f"{kw} was given as both a positional and a keyword argument! "
                                  f"({func.__name__})")
            if kw_val is MISSING:
                if argval is ...:
                    continue
                kw_val = argval
                if keywords[kw].kind == PK.POSITIONAL_ONLY:
                    arglist.append(kw_val)
                else:
                    if keywords[kw].kind == PK.KEYWORD_ONLY and kw not in kwargs:
                        raise SyntaxError(f"{kw} is a keyword-only argument, but was given as "
                                          f"positional argument! ({func.__name__})")
                    kwargs[kw] = kw_val
            argtype = keywords[kw].annotation
            argtuple = get_args(argtype)
            if not isinstance(kw_val, argtype) and not isinstance(kw_val, argtuple):
                raise TypeError(f"Argument {kw} was passed a value of type `"
                                f"{type(kw_val).__name__}`, but only accepts values of "
                                f"type `{argtype.__name__}` "
                                f"({func.__name__})")
        return func(*arglist, **kwargs)

    return cast(F, newcall)
