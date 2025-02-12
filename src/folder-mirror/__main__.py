import logging
# Lovely type hinting and cli colorful output
import typer

from .command import init, sync
from .const import FolderMirrorError

if __name__ == "__main__":
    cli = typer.Typer()

    cli.add_typer(init.cli)
    cli.add_typer(sync.cli)
    try:
        cli()
    except FolderMirrorError as e:
        log = logging.getLogger(__name__)
        log.error(e)
