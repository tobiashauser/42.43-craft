import sys
from pathlib import Path
from typing import Protocol

from craft_documents.FileSystem.Readable import Readable


class Writable(Readable, Protocol):
    """
    Represents an object that is writable.

    Inherits from `Readable`.
    """

    def __init__(self, path: Path):
        # Calling initializer of Readable
        super().__init__(path)

        # Overwrite endpoints for tests
        if "pytest" in sys.modules:
            self.__write_io = self.__write_test

    def write(
        self,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
    ):
        self.__write_io(self.path, encoding, errors, newline)

    def __write_io(
        self,
        path: Path,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
    ):
        path.write_text(self.contents)

    def __write_test(
        self,
        path: Path,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
    ):
        pass
