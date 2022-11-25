"""Simple decorators for enforcing types during runtime."""
# Flake8: noqa
from .Classes import classtypes, methtypes
from .Combined import dataclass
from .Functions import functypes

__version__ = "0.0.6"
__all__ = [
    "classtypes", "dataclass", "functypes", "methtypes"
]
