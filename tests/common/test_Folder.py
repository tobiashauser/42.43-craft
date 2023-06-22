from pathlib import Path

from draft.common.Folder import Folder


class FolderImplementation(Folder):
    def load(self):
        pass


def test_instantiation():
    input = FolderImplementation(path=Path())
