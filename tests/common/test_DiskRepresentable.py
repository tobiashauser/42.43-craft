from pathlib import Path

from draft.common.DiskRepresentable import DiskRepresentable as LiveDiskRepresentable


class DiskRepresentable(LiveDiskRepresentable):
    def __init__(self, path: Path):
        self._path = path

    def load(self):
        raise NotImplementedError


def test_initializing_TestDiskRepresentable():
    """
    Error: Cannot instantiate abstract class "TestDiskRepresentable"
    "DiskRepresentable.load" is abstract.

    -> 'def load()' must be implemented.
    """
    input = DiskRepresentable(path=Path("INVALID"))
    assert input.path == Path("INVALID")
