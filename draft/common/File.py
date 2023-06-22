from abc import ABC

from draft.common.DiskRepresentable import DiskRepresentable


class File(ABC, DiskRepresentable):
    """
    Abstract class representing a file on the disk.

    Conforming types:
    - Template (ABC)

    Subclasses should remember to call `super().__init__()`
    if they implement their own initializer, as well as
    `super().load()` when implementing their own loading
    method.
    """

    _contents: str

    @property
    def contents(self) -> str:
        return self._contents

    def __init__(self, path):
        self._path = path
        self.load()

    def load(self):
        with self.path.open("r") as file:
            self._contents = file.read()
