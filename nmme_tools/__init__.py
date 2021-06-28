"""
nmme_tools is not a real package, just a set of best practices examples.
"""

from nmme_tools.nmme_tools import meaning_of_life, meaning_of_life_url

__all__ = [
    "meaning_of_life",
    "meaning_of_life_url",
]

try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown"
