"""Simple decorators for enforcing types during runtime."""
# Flake8: noqa
from .Classes import classtypes, methtypes
from .Combined import classmeth, dataclass
from .Functions import functypes

__version__ = "0.0.2"
__all__ = [
    "classtypes", "classmeth", "dataclass", "functypes", "methtypes"
]
