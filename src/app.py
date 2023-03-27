from itertools import chain
from operator import methodcaller
from pathlib import Path

from flask import Flask, render_template, url_for, send_file, redirect

from .utils.constants import *
from .utils.helpers import format_filesize, restrict_path


app = Flask(__name__)


BASE_DIR = Path.cwd()


class File:
    @property
    def size(self):
        if self.path.is_dir() or self.path.is_symlink():
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
            self.icon_url = url_for("static", filename=FOLDER_ICON_FILENAME)
        else:
            self.icon_url = url_for("static", filename=FILE_ICON_FILENAME)
        self.url = BROWSE_BASE_URL + self.path.relative_to(BASE_DIR).as_posix()

    def __str__(self):
        return str(self.path)

    def __getattr__(self, attr):
        try:
            return getattr(self.path, attr)
        except AttributeError:
            raise AttributeError(f"File instance has no attribute '{attr}'")


@app.route("/")
def index():
    return redirect(BROWSE_BASE_URL, 301)


@app.route(BROWSE_BASE_URL)
@app.route(f"{BROWSE_BASE_URL}<path:path>")
def browse(path=""):
    base_path = restrict_path(Path(path), BASE_DIR)
    if base_path.is_file():
        # Send file if one is requested
        return send_file(
            BASE_DIR.joinpath(base_path).resolve(True), as_attachment=True
        )
    if not base_path.exists():
        # Use CWD in case base_path doesn't exist
        base_path = Path()
    items = map(File, filter(methodcaller("exists"), base_path.iterdir()))
    if base_path.resolve() != BASE_DIR:
        back_folder = File(
            base_path / "..",
            icon_url=url_for("static", filename=FOLDER_BACK_ICON_FILENAME),
        )
        items = chain([back_folder], items)
    return render_template(
        "index.html",
        parent=base_path.parent if base_path.parent != base_path else None,
        path=base_path,
        # Display directories first
        items=sorted(items, key=methodcaller("is_file")),
    )
