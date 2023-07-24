from pathlib import Path

from craft_documents.FileSystem import File, Readable, Writable


class Template(File, Writable, Readable):
    """
    A class that represents a template on the disk.

    `Template` subclasses `File` and is further
    readable and writable.

    Additionally this class implements basic functions
    to manipulate its contents.
    """

    def __init__(self, path: Path):  # + Configuration
        super().__init__(path)
