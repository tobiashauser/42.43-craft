from pathlib import Path

from draft.common.Folder import Folder


class Configuration(Folder):
    """
    A class representing the configuration's folder at '~/.config/draft/'.

    The configuration has the following structure:

    ```
    ~/.config/draft/
    ├── exercises
    ├── headers
    └── preamble.tex
    ```
    """

    def __init__(self):
        self._path = Path.home() / ".config/draft/"
        self.load()

    def load(self):
        raise NotImplementedError
