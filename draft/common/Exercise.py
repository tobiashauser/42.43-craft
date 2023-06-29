import re
from pathlib import Path

from draft.common.Configuration import Configuration
from draft.common.TexTemplate import TexTemplate


class Exercise(TexTemplate):
    """
    A class representing an exercise template.

    Exercise templates are stored in `.config/draft/exercises/`.
    They are always latex documents.
    """

    @property
    def contents(self) -> str:
        """
        Returns the entire contents.

        Use the properties `.body` and
        `.declarations` to return the parts
        that need to be included into the
        compiled document.
        """
        return super().contents

    def __init__(self, path: Path, configuration: Configuration):
        super().__init__(path, configuration)
