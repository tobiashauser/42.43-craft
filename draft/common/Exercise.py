import re
from pathlib import Path
from typing import List

from draft.common.helpers import create_list
from draft.common.Template import Template
from draft.common.TexTemplate import TexTemplate
from draft.configuration.Configuration import Configuration


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
    def supplements(self) -> List[Template]:
        return self._supplements

    def __init__(self, path: Path, configuration: Configuration):
        """
        Initialize `self` as the tex-template.

        Initialize any additional supplemental template
        files. They are declared in a yaml block in the
        tex-template under the key `supplements`.
        """
        super().__init__(path, configuration)

        self._supplements: List[Template] = []
        for path in create_list(self.yaml.get("supplements", [])):
            self._supplements.append(
                Template(self.configuration, self.path.parent / path)
            )

    def load(self):
        """
        Load the contents of the exercise template.
        """
        with self.path.open() as file:
            self._contents = file.read()
