import re
from pathlib import Path
from typing import List

from draft.common.Configuration import Configuration
from draft.common.helpers import create_list
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

    @property
    def supplements(self) -> List[Path]:
        return self._supplements

    def __init__(self, path: Path, configuration: Configuration):
        """
        In addition to initializing self with the tex template,
        also initialize any supplemental templates declared under
        the key `supplements` in the yaml block.
        """
        super().__init__(path, configuration)

        self._supplements: List[Path] = []
        for path in create_list(self.yaml.get("supplements", [])):
            self._supplements.append(self.path.parent / path)

    def load(self):
        """
        Load the contents of the exercise template.

        Initialize any additional supplemental template
        files. They are declared in a yaml block in the
        tex-template under the key `supplements`.
        """
        with self.path.open() as file:
            self._contents = file.read()
