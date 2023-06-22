from abc import ABC

from draft.common.DiskRepresentable import DiskRepresentable


class Folder(ABC, DiskRepresentable):
    """
    Abstract class representing a folder on the disk.

    Conforming types:
    - Configuration
    """

    def __init__(self, path):
        self._path = path
        self.load()
