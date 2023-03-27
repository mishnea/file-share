from math import log10, log
from pathlib import Path

from .constants import SIZE_UNITS


def restrict_path(unsafe_path, base_path):
    """Return `unsafe_path` relative to `base_path`"""

    unsafe_path = Path(unsafe_path).resolve()
    base_path = Path(base_path).resolve()
    try:
        return unsafe_path.relative_to(base_path)
    except ValueError:
        return Path()


def format_filesize(size):
    i = int(log(size, 1024))
    size = size / 1024**i
    # Calculate number of decimal points to show
    p = max(2 - int(log10(size)), 0)
    size = round(size, p)
    if p == 0:
        return f"{int(size)}{SIZE_UNITS[i]}"
    return f"{size:.{p}f}{SIZE_UNITS[i]}"
