import shutil
import sys
from copy import deepcopy
from pathlib import Path
from typing import Protocol, Self

from craft_documents.FileSystem.DiskRepresentable import DiskRepresentable


class Copyable(DiskRepresentable, Protocol):
    """
    Represents an object that can be copied
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
            self.__copy_io = self.__copy_test

    def copy(self, newPath: Path) -> Self:
        """
        I/O. Copy the resource to the new location,
        overwriting if the new location already exists.
        """
        copy: Self = deepcopy(self)
        copy._path = self.__copy_io(newPath)
        return copy

    def __copy_io(self, newPath: Path) -> Path:
        if self.path.is_file():
            return shutil.copy2(self.path, newPath, follow_symlinks=False)
        elif self.path.is_dir():
            return shutil.copytree(self.path, newPath, symlinks=True, dirs_exist_ok=True)
        else:
            raise FileNotFoundError()

    def __copy_test(self, newPath: Path) -> Path:
        return newPath
