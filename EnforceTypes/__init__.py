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
