import itertools
from typing import Iterable
import hashlib
from .sync_action import *

def hash_file_sha256(file_path: Path) -> bytes:
    hash = hashlib.sha256()
                
    with file_path.open('rb') as file:
        while chunk := file.read(CHUNK_SIZE):
            hash.update(chunk)

    return hash.digest()

def deletion_walk(root_src: Path, root_dst: Path) -> Iterable[SyncAction]:
    # Walking down to top, we need to remove files before unlinking directories
    for root, dirs, files in root_dst.walk(top_down=False):
        def deletion_path_generator(iter):
            for element in iter:
                # Construct source expected path from it's root, middle part of the directory structure and a filename or foldername
                src = root_src / root.relative_to(root_dst) / element
                dst = root / element
                yield src, dst

        for src, dst in deletion_path_generator(dirs):
            if src.exists():
                yield PreserveDirectory(dst)
            else:
                yield RemoveDirectory(dst)
        
        for src, dst in deletion_path_generator(files):
            if src.exists():
                yield PreserveFile(dst)
            else:
                yield RemoveFile(dst)

def creation_walk(root_src: Path, root_dst: Path) -> Iterable[SyncAction]:
    # Walking top to down, we need to create directiories before we create files in them
    for root, dirs, files in root_src.walk(top_down=True):
        def creation_path_generator(iter):
            for element in iter:
                # Construct source expected path from it's root, middle part of the directory structure and a filename or foldername
                src = root / element
                dst = root_dst / root.relative_to(root_src) / element
                yield src, dst

        for src, dst in creation_path_generator(dirs):
            if dst.exists():
                yield PreserveDirectory(dst)
            else:
                yield CreateDirectory(dst)

        for src, dst in creation_path_generator(files):
            if dst.exists():
                if hash_file_sha256(src) != hash_file_sha256(dst):
                    yield CopyFileContentsChunked(src_path=src, dst_path=dst)
                else:
                    yield PreserveFile(dst)

            else:
                yield CreateFile(dst)
                yield CopyFileContentsChunked(src_path=src, dst_path=dst)

def sync_walk(root_src: Path, root_dst: Path) -> Iterable[SyncAction]:
    return itertools.chain(deletion_walk(root_src, root_dst), creation_walk(root_src, root_dst))