from itertools import count
import multiprocessing as mp
from pathlib import Path
from tkinter import Tk, StringVar
from tkinter.filedialog import askdirectory
from tkinter.ttk import Entry, Frame, Label, Button

from . import app
from .app import app as flask_app


def select_dir():
    path = askdirectory(mustexist=True, title="Select directory to serve")
    if not path:
        return
    base_dir.set(path)


def start():
    global p

    set_gui(True)
    app.BASE_DIR = Path(base_dir.get())
    # Replace with different WSGI server
    p = mp.Process(target=flask_app.run, kwargs=dict(host=host.get(), port=port.get()))
    p.start()


def stop():
    p.terminate()
    p.join()
    set_gui(False)


def quit(*_):
    if p.is_alive():
        p.terminate()
        p.join()


def set_gui(running: bool):
    if running:
        start_button.grid_remove()
        stop_button.grid()
        state = "disabled"
    else:
        stop_button.grid_remove()
        start_button.grid()
        state = "normal"
    for widget in disable_list:
        widget.config(state=state)


padding = {"padx": 10, "pady": 10}


# Initialise
p = mp.Process()
root = Tk()
root.bind("<Destroy>", quit)
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
# Frame contains entry and button for correct alignment
base_dir_frm = Frame(frm)
base_dir_frm.grid(row=row, column=1, **padding)
directory_entry = Entry(base_dir_frm, textvariable=base_dir)
directory_entry.grid(row=row, column=1)
directory_button = Button(base_dir_frm, text="...", width=2, command=select_dir)
directory_button.grid(row=row, column=2)

# Host
host = StringVar(value="0.0.0.0")
row = next(counter)
Label(frm, text="Host").grid(row=row, column=0, sticky="E", **padding)
host_entry = Entry(frm, textvariable=host)
host_entry.grid(row=row, column=1, sticky="EW", **padding)

# Port
port = StringVar(value="5000")
row = next(counter)
Label(frm, text="Port").grid(row=row, column=0, sticky="E", **padding)
port_entry = Entry(frm, textvariable=port)
port_entry.grid(row=row, column=1, sticky="EW", **padding)

# Start/Stop
row = next(counter)
start_button = Button(frm, text="Start", command=start)
start_button.grid(row=row, column=0, columnspan=2, **padding)
stop_button = Button(frm, text="Stop", command=stop)
stop_button.grid(row=row, column=0, columnspan=2, **padding)
stop_button.grid_remove()

# Widgets to enable/disable
disable_list = [
    directory_entry,
    directory_button,
    host_entry,
    port_entry,
]

# Run
root.mainloop()
