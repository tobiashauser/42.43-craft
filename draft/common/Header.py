from pathlib import Path

from draft.common.TexTemplate import TexTemplate


class Header(TexTemplate):
    """
    A class representing a header template.

    Header templates are stored in `.config/draft/headers/`.
    They are always latex documents.
    """

    def load(self):
        """
        Remove the input statement of the preamble from the contents.
        """
        with self.path.open("r") as file:
            contents = file.read()

        self._contents = Header.remove_include_preamble(contents)
