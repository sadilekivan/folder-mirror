import logging
import typer
from pathlib import Path
from typing import Optional

from ..config_log import *
from ..const import *
from ..path_link import PathLink
from .. import tree_walk
from ..interval_delay import IntervalDelay

cli = typer.Typer()

@cli.command()
def sync(
        mirror: Path,
        sync_interval: int = 30,
        log_level: LoggingLevelArg = LoggingLevelArg.Info.value,
        log_path: Optional[Path] = None
    ):
    configure_logging(log_level, log_path)
    log = logging.getLogger(__name__)
    log.info(f"Starting folder-mirror sync command")

    mirror_data_path = mirror / MIRROR_DATA_FOLDER_NAME
    mirror_src_link_path = PathLink(mirror / MIRROR_SOURCE_LINK_PATH_NAME)

    if not mirror.is_dir() or not mirror_data_path.is_dir() or not mirror_src_link_path.is_file():
        raise FolderMirrorError(f"{mirror.absolute()} is not a initialized folder-mirror")

    source = mirror_src_link_path.read_link_path()

    if not source.is_dir():
        raise FolderMirrorError(f"Source folder {source.absolute()} does not exist")

    if sync_interval < SYNC_INTERVAL_LIMIT:
        raise FolderMirrorError(f"Sync interval should be above or equal to {SYNC_INTERVAL_LIMIT} seconds. Supplied {sync_interval}")
    
    log.info(f"Syncing {source.absolute()} -> {mirror.absolute()}")

    interval_delay = IntervalDelay(sync_interval)
    try:
        while True:
            # TODO Get all actions, reorder them with removal of files first, creation of directories and then copy all new files in parallel to speed things up
            log.debug(f"Walking directories")
            action_list = tree_walk.sync_walk(source, mirror_data_path)
            for action in action_list:
                action.action_run()
            interval_delay.sleep()
    except KeyboardInterrupt:
        log.info(f"Ctrl-c registered, exiting loop")

    log.info(f"folder-mirror syncing done")