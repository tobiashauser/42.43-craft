from abc import ABC
from pathlib import Path

from draft.common.File import File


class Template(File, ABC):
    """
    A abstract class representing a template, that is a file
    on the disk.

    Conforming types are:
    - Preamble
    - Header
    - ExerciseTemplate
    """

    def __init__(self, path: Path):
        super().__init__(path=path)
