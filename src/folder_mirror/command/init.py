import logging
import typer
from pathlib import Path
from typing import Optional

from ..config_log import *
from ..const import *
from ..path_link import PathLink

cli = typer.Typer()

@cli.command()
def init(
        source: Path,
        mirror: Path,
        log_level: LoggingLevelArg = LoggingLevelArg.Info.value,
        log_path: Optional[Path] = None
    ):
    configure_logging(log_level, log_path)
    log = logging.getLogger(__name__)
    log.info(f"Starting folder-mirror init command")

    # Check if paths are valid
    if not source.exists():
        raise FolderMirrorError(f"{source.absolute()} path needs to exist")

    if not source.is_dir():
        raise FolderMirrorError(f"{source.absolute()} path needs be a folder")
    
    if mirror.exists():
        raise FolderMirrorError(f"{mirror.absolute()} path needs to not exist for it to be initialized")
    
    log.info(f"Initializing folder-mirror at '{mirror.absolute()}'")

    # folder-mirror paths
    mirror_data_path = mirror / MIRROR_DATA_FOLDER_NAME
    mirror_src_link_path = PathLink(mirror / MIRROR_SOURCE_LINK_PATH_NAME)
    
    # folder-mirror init operations
    mirror.mkdir()
    mirror_data_path.mkdir()
    mirror_src_link_path.write_link_path(source)

    log.info(f"folder-mirror init done")