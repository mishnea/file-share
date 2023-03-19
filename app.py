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
    FOLDER_ICON_FILENAME = "icons/folder.svg"
    FILE_ICON_FILENAME = "icons/document.svg"

    @property
    def size(self):
        if self.is_dir():
            return ""
        return format_filesize(self.path.stat().st_size)

    def __init__(self, path, icon_url=None):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"File does not exist: {path}")
        # Set icon_url with fallback
        if icon_url is not None:
            self.icon_url = icon_url
        elif self.is_dir():
            self.icon_url = url_for("static", filename=self.FOLDER_ICON_FILENAME)
        else:
            self.icon_url = url_for("static", filename=self.FILE_ICON_FILENAME)

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
        back_folder = File(
            base_path / "..",
            icon_url=url_for("static", filename="icons/folder-left.svg"),
        )
        items = chain([back_folder], items)
    return render_template(
        "index.html",
        parent=base_path.parent if base_path.parent != base_path else None,
        path=base_path,
        # Display directories first
        items=sorted(items, key=methodcaller("is_file")),
    )
