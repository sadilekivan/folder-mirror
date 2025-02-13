# folder-mirror
## Description

This program is designed to sync files, including removal.

To prevent possible data loss at the `mirror` path (In case `mirror` is carelessly selected with already importnant other data that wont be in source), this program requires it's own mirror folder with predefined structure.

A `mirror` folder can be initialized at a non-existing path (needs to have a parent). When initializing a mirror you need both a `source` to synchronize to mirror and a `mirror` path where to initialize the mirror.

If you already have a initialized `mirror` folder you can just sync source to it by specifing it's path (`mirror` folder remembers it's `source`).

## `mirror` folder structure
The `mirror` root path will have the following structure:

```
mirror-root             (folder: selected mirror path)
│   source-link-path    (file: contains source path to ensure same source is used for the mirror)    
└───data                (folder: latest copy of source folder)
    └───...             (source folder contents here)
```

## Usage

To test out this folder-mirror program please initialize a `mirror` and then sync to it like so:

```bash
~\folder-mirror>
py -m src.folder_mirror init dummy_env/original dummy_env/mirror --log-level debug
py -m src.folder_mirror sync dummy_env/mirror --sync-interval 3 --log-level debug --log-path dummy_env/original/folder_mirror.log
```

Notice how intial data and any changes are copied together with the update of the log. You can leave it running for a while to see how sync handles the growing log file.

Feel free to drop in large trees of folders and files, I tested with this nice repo with [4k wallpapers (mostly)](https://github.com/makccr/wallpapers/tree/master)

You can also install this package with (`-e` makes the installation editable, it will just point to this local repo):

```shell
~\folder-mirror>
pip install -e .
```

And then run the package from anywhere with:

```shell
~\folder-mirror>
py -m folder_mirror init dummy_env/original dummy_env/mirror --log-level debug
py -m folder_mirror sync dummy_env/mirror --sync-interval 3 --log-level debug --log-path dummy_env/original/folder_mirror.log
```

## Dependencies

This repo only requires `typer` for the cli interface.

Optionaly if you let `human-readable` install you get nice file size units in the log

Both will install by default with `pip`
