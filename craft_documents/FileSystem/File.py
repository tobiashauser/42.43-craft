from pathlib import Path

from craft_documents.FileSystem.Copyable import Copyable
from craft_documents.FileSystem.Moveable import Movable
from craft_documents.FileSystem.Resource import Resource


class File(Resource, Copyable, Movable):
    """
    Class that represents a file on the disk.

    It subclasses `Resource` as well as conforms
    to the protocols `Copyable` and `Movable`.
    """

    _path: Path

    def __init__(self, path: Path):
        super().__init__(path)
