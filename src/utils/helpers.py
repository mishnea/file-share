from math import log10, log
from pathlib import Path

from .constants import SIZE_UNITS


def restrict_path(unsafe_path, base_path):
    """Return `unsafe_path` resolved with base `base_path` if it's relative, else `base_path`"""

    base_path = Path(base_path).resolve()
    unsafe_path = Path(base_path / unsafe_path).resolve()
    if unsafe_path.is_relative_to(base_path):
        return unsafe_path
    return base_path


def format_filesize(size):
    if size == 0:
        return "0B"
    i = int(log(size, 1024))
    size = size / 1024**i
    # Calculate number of decimal points to show
    p = max(2 - int(log10(size)), 0)
    size = round(size, p)
    if p == 0:
        return f"{int(size)}{SIZE_UNITS[i]}"
    return f"{size:.{p}f}{SIZE_UNITS[i]}"
