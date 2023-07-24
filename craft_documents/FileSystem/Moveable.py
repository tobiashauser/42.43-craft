import shutil
import sys
from abc import abstractmethod
from pathlib import Path
from typing import Protocol

from craft_documents.FileSystem.DiskRepresentable import DiskRepresentable


class Movable(DiskRepresentable, Protocol):
    """
    Represents an object that can be moved
    to a new location.

    Inherits from `DiskRepresentable`.
    """

    _path: Path

    def __init__(self, path: Path):
        """Initializing an object that is Movable."""
        # Calling initializer of DiskRepresentable
        super().__init__(path)

        # Overwrite endpoints when testing
        if "pytest" in sys.modules:
            self.__move_io = self.__move_test

    def move(self, newPath: Path):
        """
        Move the resource to a new location, overwriting
        if the new location already exists.
        """
        self._path = self.__move_io(newPath)

    def __move_io(self, newPath: Path) -> Path:
        return shutil.move(self.path, newPath)

    def __move_test(self, newPath: Path) -> Path:
        return newPath
