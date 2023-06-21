from abc import abstractmethod
from pathlib import Path
from typing import Protocol


class DiskRepresentable(Protocol):
    """
    A protocol representing a file or folder on the disk.
    """

    _path: Path

    @property
    def path(self) -> Path:
        return self._path

    @abstractmethod
    def load(self):
        """
        Loads the data from the disk.

        Override this endpoint in tests to load the data from
        a folder in this directory or to instantiate the type
        with mock data.
        """
        raise NotImplementedError
