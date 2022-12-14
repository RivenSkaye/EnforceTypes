from typing import Any, Type
import typing_inspect as ti  # type: ignore


def resolve_types(tp: Type) -> Type:
    if tp is Any or ti.is_generic_type(tp):
        return object
    if ti.is_union_type(tp) or ti.is_new_type(tp) or ti.is_classvar(tp):
        return tp
    elif ti.is_literal_type(tp):
        return str
    if ti.is_typevar(tp):
        tp = ti.get_bound(tp)
    if ti.is_generic_type(tp):
        tp = ti.get_origin(tp)
    return tp if tp is not None else type(None)
