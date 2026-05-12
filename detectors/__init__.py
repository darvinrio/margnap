"""
__init__.py

Detectors
"""

from .em_dash import find_em_dashes
from .not_just_but import find_not_but_also
from .triad import find_triads

__all__ = ["find_em_dashes", "find_not_but_also", "find_triads"]
