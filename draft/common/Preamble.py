from pathlib import Path

from draft.common.TexTemplate import TexTemplate
from draft.configuration.Configuration import Configuration


class Preamble(TexTemplate):
    """
    A class representing the preamble.

    This class customizes the loading function
    in order to strip the document environment
    from its contents.
    """

    def load(self):
        """
        Remove the document environment.
        """
        with self.path.open("r") as file:
            self._contents = file.read()
        self.remove_document_body()
