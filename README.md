# File Share

## Develop

Loopback only:

`env PYTHONPATH=$PYTHONPATH:.. python -m file-share -d`

LAN:

`env PYTHONPATH=$PYTHONPATH:.. python -m file-share -d -h 0.0.0.0`

## Deployment

Serve your home directory:

`python -m file-share -h 0.0.0.0 -b ~`

More configuration can be found using the `--help` flag

## Attributions

- Icons: [www.svgrepo.com/author/scarlab/](https://www.svgrepo.com/collection/scarlab-oval-line-icons)
