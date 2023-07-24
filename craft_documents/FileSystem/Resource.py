from pathlib import Path

from craft_documents.FileSystem.DiskRepresentable import DiskRepresentable


class Resource(DiskRepresentable):
    """
    A resource in the file system such as a folder or file.
    """

    def __init__(self, path: Path):
        # Calling initializer of Movable
        super().__init__(path)
