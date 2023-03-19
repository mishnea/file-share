from argparse import ArgumentParser
from pathlib import Path

from .app import app


parser = ArgumentParser(
    prog="File Share",
    description="File server with a mobile friendly web UI for sharing and receiving files over a local network",
    add_help=False,
)

parser.add_argument("--help", action="store_true", help="Show a help message")

parser.add_argument("-d", "--debug", action="store_true", help="Use Flask's debug mode")

parser.add_argument(
    "-h",
    "--host",
    default="127.0.0.1",
    help="Specify the hostname. Use 0.0.0.0 to allow all incoming connections",
)

parser.add_argument("-p", "--port", default="5000", help="Specify the port")

args = parser.parse_args()

if args.help:
    parser.print_help()
else:
    print("Serving directory", Path.cwd())
    if args.debug:
        app.run(host=args.host, port=args.port, debug=True)
    else:
        # Replace with different WSGI server
        app.run(host=args.host, port=args.port)
