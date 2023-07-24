import sys
from pathlib import Path
from typing import Protocol


class DiskRepresentable(Protocol):
    """Represents an object that is present in the file system."""

    _path: Path

    def __init__(self, path: Path):
        """
        Initialize an object that is present on the disk.

        Raises a `FileNotFoundError` if the object does
        not exist on the disk.
        """
        # Calling initializer of Protocol
        super().__init__()

        # Overwrite endpoints when testing
        if "pytest" in sys.modules:
            DiskRepresentable.__validate_path_io = DiskRepresentable.__validate_path_test

        # Initialize properties
        if DiskRepresentable.validate_path(path):
            self._path: Path = path
        else:
            raise FileNotFoundError()

    @property
    def path(self) -> Path:
        """The path to the object."""
        return self._path

    @staticmethod
    def validate_path(path: Path) -> bool:
        """
        I/O. Check if the objects exists on the disk.

        Always returns `True` when testing. Overwrite
        `DiskRepresentable.__validate_path_test` to
        change this behaviour.
        """
        return DiskRepresentable.__validate_path_io(path)

    @staticmethod
    def __validate_path_io(path: Path) -> bool:
        return path.exists()

    @staticmethod
    def __validate_path_test(path: Path) -> bool:
        return True
