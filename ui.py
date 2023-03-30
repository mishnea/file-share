from itertools import count
from pathlib import Path
from tkinter import Tk, StringVar
from tkinter.filedialog import askdirectory
from tkinter.ttk import Entry, Frame, Label, Button

from src import app
from src.app import app as flask_app


def select_dir():
    path = askdirectory(mustexist=True, title="Select directory to serve")
    if not path:
        return
    base_dir.set(path)


def start():
    root.destroy()
    app.BASE_DIR = Path(base_dir.get())
    print("Serving directory", app.BASE_DIR)
    # Replace with different WSGI server
    flask_app.run(host=host.get(), port=port.get())


padding = {"padx": 10, "pady": 10}


# Initialise
root = Tk()
frm = Frame(root, padding=10)
frm.master.title("file-share")
frm.grid()


# Add widgets
# Make changing order of rows less painful
counter = count()

# Base directory
base_dir = StringVar(value=Path.cwd())
row = next(counter)
Label(frm, text="Directory").grid(row=row, column=0, sticky="E", **padding)
base_dir_frm = Frame(frm)
base_dir_frm.grid(row=row, column=1, **padding)
Entry(base_dir_frm, textvariable=base_dir).grid(row=row, column=1)
Button(base_dir_frm, text="...", width=2, command=select_dir).grid(row=row, column=2)

# Host
host = StringVar(value="0.0.0.0")
row = next(counter)
Label(frm, text="Host").grid(row=row, column=0, sticky="E", **padding)
Entry(frm, textvariable=host).grid(row=row, column=1, sticky="EW", **padding)

# Port
port = StringVar(value="5000")
row = next(counter)
Label(frm, text="Port").grid(row=row, column=0, sticky="E", **padding)
Entry(frm, textvariable=port).grid(row=row, column=1, sticky="EW", **padding)

# Start
row = next(counter)
Button(frm, text="Start", command=start).grid(
    row=row, column=0, columnspan=2, **padding
)


# Run
root.mainloop()
