from argparse import ArgumentParser
from pathlib import Path

from src import app
from src.app import app as flask_app
from src.gui import GUI


parser = ArgumentParser(
    prog="File Share",
    description="File server with a mobile friendly web UI for sharing and receiving files over a local network",
    add_help=False,
)

parser.add_argument("-h", "--help", action="store_true", help="Show a help message")

parser.add_argument(
    "-n", "--no-gui", action="store_true", help="Don't show a setup GUI"
)

parser.add_argument("-d", "--debug", action="store_true", help="Use Flask's debug mode")

parser.add_argument(
    "-H",
    "--host",
    default="127.0.0.1",
    help="Specify the hostname. Use 0.0.0.0 to allow all incoming connections",
)

parser.add_argument("-p", "--port", default="5000", help="Specify the port")

parser.add_argument(
    "-b",
    "--base-dir",
    type=Path,
    default=Path.cwd(),
    help="Set the directory which is served",
)

args = parser.parse_args()

if args.help:
    parser.print_help()
elif not (args.no_gui or args.debug):
    GUI(args.host, args.port, args.base_dir).mainloop()
else:
    app.BASE_DIR = args.base_dir
    print("Serving directory", app.BASE_DIR)
    if args.debug:
        flask_app.run(host=args.host, port=args.port, debug=True)
    else:
        # Replace with different WSGI server
        flask_app.run(host=args.host, port=args.port)
