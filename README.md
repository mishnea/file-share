# File Share

## Setup

1. `python -m venv .venv`
2. Depends on OS:
   - Linux: `source .venv/bin/activate`
   - Windows: `.\.venv\Scripts\activate.ps1`
3. `pip install -r requirements.txt`

## Develop

Loopback only:

`python main.py -d`

LAN:

`python main.py -d -h 0.0.0.0`

With Setup UI:

`python main.py --ui`

## Build

`pyinstaller file-share.spec`

## Run

Download the binary for your OS and run it

## Attributions

- Icons: [www.svgrepo.com/author/scarlab/](https://www.svgrepo.com/collection/scarlab-oval-line-icons)
