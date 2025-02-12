import logging
from pathlib import Path
from enum import Enum

class LoggingLevelArg(Enum):
    Debug = 'debug'
    Info = 'info'
    Warning = 'warn'
    Error = 'error'

def configure_logging(level: LoggingLevelArg, log_path: Path):
    handlers = [logging.StreamHandler()] + (
        [] if log_path == None else [logging.FileHandler(log_path)]
    )
    
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(name)s %(message)s',
        level=logging._nameToLevel[level.name.upper()],
        handlers=handlers
    )