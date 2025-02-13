from pathlib import Path
from folder_mirror import tree_walk, sync_action as sa

SRC_PATH = Path(__file__).parent / 'test_env/original'
DST_PATH = Path(__file__).parent / 'test_env/mirror'

def test_tree_walk():
    expected_action_list = [
        sa.RemoveDirectory,
        sa.PreserveFile,
        sa.RemoveFile,
        sa.CreateDirectory,
        sa.CreateFile,
        sa.CopyFileContentsChunked,
        sa.PreserveFile
    ]

    action_list = list(tree_walk.sync_walk(SRC_PATH, DST_PATH))
    print(action_list)
    for (action, cls) in zip(action_list, expected_action_list):
        assert type(action) == cls