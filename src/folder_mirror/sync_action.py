import logging
log = logging.getLogger(__name__)
from pathlib import Path

try:
    import human_readable
    def convert_bytes(size: int) -> str:
        return human_readable.file_size(size)
except ImportError:
    def convert_bytes(size: int) -> str:
        return f"{size} Bytes"
        

CHUNK_SIZE = 1024 # Copy over in chunks of 1 kibibit

class SyncAction:
    def __init__(self, path: Path):
        self.path = path

    def action_run(self):
        log.debug(f"Empty sync action ran on {self.path}")

class PreserveFile(SyncAction):
    def action_run(self):
        log.debug(f"Preserving file at {self.path}")

class PreserveDirectory(SyncAction):
    def action_run(self):
        log.debug(f"Preserving folder at {self.path}")

class RemoveFile(SyncAction):
    def action_run(self):
        log.info(f"Removing file at {self.path}")
        self.path.unlink()

class RemoveDirectory(SyncAction):
    def action_run(self):
        log.info(f"Removing folder at {self.path}")
        self.path.rmdir()

class CreateFile(SyncAction):
    def action_run(self):
        log.info(f"Creating file at {self.path}")
        self.path.touch()

class CreateDirectory(SyncAction):
    def action_run(self):
        log.info(f"Creating folder at {self.path}")
        self.path.mkdir()


class CopyFileContentsWhole(SyncAction):
    """Deprecated, use `CopyFileContentsChunked` to spare RAM in case of large files"""
    def __init__(self, path: Path, data: bytes):
        self.path = path
        self.data = data

    def action_run(self):
        file_size = convert_bytes(len(self.data))
        log.info(f"Copying {file_size} bytes to {self.path}")
        self.path.write_bytes(self.data)

class CopyFileContentsChunked(SyncAction):
    def __init__(self, src_path: Path, dst_path: Path):
        self.src_path = src_path
        self.dst_path = dst_path

    def action_run(self):
        bytes_count = 0
        log.debug(f"Copying {self.src_path} contents to {self.dst_path}")

        with self.src_path.open('rb') as src:
            with self.dst_path.open('wb') as dst:
                while True:
                    chunk = src.read(CHUNK_SIZE)
                    chunk_len = len(chunk)
                    
                    if chunk_len == 0:
                        break

                    dst.write(chunk)
                    bytes_count += chunk_len

        file_size = convert_bytes(bytes_count)
        log.info(f"Copied {file_size} into {self.dst_path.name}")

