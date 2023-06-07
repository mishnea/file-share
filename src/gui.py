from itertools import count
import multiprocessing as mp
from pathlib import Path
from tkinter import Tk, StringVar
from tkinter.filedialog import askdirectory
from tkinter.ttk import Entry, Frame, Label, Button

from . import app
from .app import app as flask_app


PADDING = {"padx": 10, "pady": 10}


class GUI(Frame):
    def __init__(self, host, port, base_dir):
        self.p = mp.Process()
        self.root = Tk()
        self.root.bind("<Destroy>", lambda *_: self._stop())
        self.root.title("file-share")
        super().__init__(self.root, padding=10)
        self.grid()

        # Set up widgets
        self.host = StringVar(value=host)
        self.port = StringVar(value=port)
        self.base_dir = StringVar(value=base_dir)
        self._init_widgets()

    def _init_widgets(self):
        """Add necessary widgets to self"""

        # Make changing order of rows less painful
        counter = count()

        # Base directory
        row = next(counter)
        Label(self, text="Directory").grid(row=row, column=0, sticky="E", **PADDING)
        # New frame contains entry and button for correct alignment
        base_dir_frm = Frame(self)
        base_dir_frm.grid(row=row, column=1, **PADDING)
        directory_entry = Entry(base_dir_frm, textvariable=self.base_dir)
        directory_entry.grid(row=row, column=1)
        directory_button = Button(
            base_dir_frm, text="...", width=2, command=self._select_dir
        )
        directory_button.grid(row=row, column=2)

        # Host
        row = next(counter)
        Label(self, text="Host").grid(row=row, column=0, sticky="E", **PADDING)
        host_entry = Entry(self, textvariable=self.host)
        host_entry.grid(row=row, column=1, sticky="EW", **PADDING)

        # Port
        row = next(counter)
        Label(self, text="Port").grid(row=row, column=0, sticky="E", **PADDING)
        port_entry = Entry(self, textvariable=self.port)
        port_entry.grid(row=row, column=1, sticky="EW", **PADDING)

        # Start/Stop
        row = next(counter)
        self.start_button = Button(self, text="Start", command=self._on_start_button)
        self.start_button.grid(row=row, column=0, columnspan=2, **PADDING)
        self.stop_button = Button(self, text="Stop", command=self._on_stop_button)
        self.stop_button.grid(row=row, column=0, columnspan=2, **PADDING)
        self.stop_button.grid_remove()

        # Widgets to enable/disable
        self.disable_list = [
            directory_entry,
            directory_button,
            host_entry,
            port_entry,
        ]

    def _on_start_button(self):
        """Change GUI state and stop the server process"""

        # Change GUI state
        self.start_button.grid_remove()
        self.stop_button.grid()
        for widget in self.disable_list:
            widget.config(state="disabled")
        # Start the server
        self._start()

    def _on_stop_button(self):
        """Stop the server process and change GUI state"""

        # Stop the process
        self._stop()
        # Change GUI state
        self.stop_button.grid_remove()
        self.start_button.grid()
        for widget in self.disable_list:
            widget.config(state="normal")

    def _select_dir(self):
        """Open a dialog to choose folder for base_dir"""

        path = askdirectory(mustexist=True, title="Select directory to serve")
        if not path:
            return
        self.base_dir.set(path)

    def _start(self):
        """Start the server process"""

        if self.p.is_alive():
            return
        app.BASE_DIR = Path(self.base_dir.get())
        # Replace with different WSGI server
        self.p = mp.Process(
            target=flask_app.run,
            kwargs=dict(host=self.host.get(), port=self.port.get()),
        )
        self.p.start()

    def _stop(self):
        """Stop the server process"""

        if not self.p.is_alive():
            return
        self.p.terminate()
        self.p.join()
