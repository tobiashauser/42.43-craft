from abc import ABC, abstractmethod
from pathlib import Path


class Folder(ABC):
    """
    An abstraction over a directory on the disk.
    """

    @property
    @abstractmethod
    def path(self) -> Path:
        pass

    @abstractmethod
    def validate(self):
        pass
