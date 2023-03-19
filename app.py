from itertools import chain
from math import log10, log
from operator import methodcaller
from pathlib import Path

from flask import Flask, render_template, url_for, send_file


app = Flask(__name__)


size_units = [
    "B",
    "KiB",
    "MiB",
    "GiB",
    "TiB",
]


def format_filesize(size):
    i = int(log(size, 1024))
    size = size / 1024**i
    # Calculate number of decimal points to show
    p = max(2 - int(log10(size)), 0)
    size = round(size, p)
    if p == 0:
        return f"{int(size)}{size_units[i]}"
    return f"{size:.{p}f}{size_units[i]}"


class File:
    FOLDER_ICON_FILENAME = "icons/folder-svgrepo-com.svg"
    FILE_ICON_FILENAME = "icons/document-svgrepo-com.svg"

    @property
    def icon_url(self):
        if self.is_dir():
            return url_for("static", filename=self.FOLDER_ICON_FILENAME)
        return url_for("static", filename=self.FILE_ICON_FILENAME)

    @property
    def size(self):
        if self.is_dir():
            return ""
        return format_filesize(self.path.stat().st_size)

    def __init__(self, path):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"File does not exist: {path}")

    def __str__(self):
        return str(self.path)

    def __getattr__(self, attr):
        try:
            return getattr(self.path, attr)
        except AttributeError:
            raise AttributeError(f"File instance has no attribute '{attr}'")


@app.route("/")
@app.route("/<path:path>")
def hello_world(path=""):
    base_path = Path() / path
    if not base_path.resolve().is_relative_to(Path.cwd()):
        # Don't allow user to escape CWD
        base_path = Path()
    if base_path.is_file():
        # Send file if one is requested
        return send_file(
            base_path.resolve(True).relative_to(Path.cwd()), as_attachment=True
        )
    if not base_path.exists():
        # Use CWD in case base_path doesn't exist
        base_path = Path()
    items = map(File, base_path.iterdir())
    if base_path.resolve() != Path.cwd():
        items = chain([File(base_path / "..")], items)
    return render_template(
        "index.html",
        parent=base_path.parent if base_path.parent != base_path else None,
        path=base_path,
        # Display directories first
        items=sorted(items, key=methodcaller("is_file")),
    )
