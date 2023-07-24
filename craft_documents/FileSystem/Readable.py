import sys
from pathlib import Path
from typing import Protocol

from craft_documents.FileSystem.DiskRepresentable import DiskRepresentable


class Readable(DiskRepresentable, Protocol):
    """
    Represents an object whose contents can be
    read as a string.

    Inherits from `DiskRepresentable`.
    """

    _contents: str = ""

    def __init__(self, path: Path):
        # Calling initializer of DiskRepresentable
        super().__init__(path)

        # Overwrite endpoints for tests
        if "pytest" in sys.modules:
            self.__read_io = self.__read_test

    @property
    def contents(self) -> str:
        return self._contents

    def read(self, path: Path):
        self._contents = self.__read_io(path)

    def __read_io(self, path: Path) -> str:
        return path.read_text()

    def __read_test(self, path: Path) -> str:
        raise NotImplementedError
