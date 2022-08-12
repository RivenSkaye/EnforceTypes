"""Simple decorators for enforcing types during runtime."""
from functools import wraps
from inspect import signature, _ParameterKind as PK
from types import FunctionType
from typing import Any, Callable, Type, TypeVar, cast, get_args

__all__ = [
    "classtypes", "functypes"
]

__version__ = "0.0.2"


class _MISSING:
    pass


MISSING = _MISSING()
T = TypeVar("T")
F = TypeVar("F", bound=Callable)


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


def classtypes(cls: Type[T]) -> Type[T]:
    """For use as class decorator. Enforces types in ``init``"""
    oldinit: Callable = getattr(cls, "__init__")  # type: ignore
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
            argtype = keywords[kw].annotation
            argtuple = get_args(argtype)
            if not isinstance(kw_val, argtype) and not isinstance(kw_val, argtuple):
                raise TypeError(f"Argument {kw} was passed a value of type `"
                                f"{type(kw_val).__name__}`, but only accepts values of "
                                f"type `{argtype.__name__}` "
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
            argtype = keywords[kw].annotation
            argtuple = get_args(argtype)
            if not isinstance(kw_val, argtype) and not isinstance(kw_val, argtuple):
                raise TypeError(f"Argument {kw} was passed a value of type `"
                                f"{type(kw_val).__name__}`, but only accepts values of "
                                f"type `{argtype.__name__}` "
                                f"({meth.__name__})")
        return meth(selfcls, *arglist, **kwargs)

    return cast(F, newcall)
