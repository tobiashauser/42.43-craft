from pathlib import Path

from draft.common.DiskRepresentable import DiskRepresentable


class Configuration(DiskRepresentable):
    """
    A class representing the configuration's folder at '~/.config/draft/'.

    The configuration has the following structure:

    ```
    ~/.config/draft/
    └── templates
        ├── exercises
        ├── headers
        └── preamble.tex
    ```
    """

    def __init__(self):
        self._path = Path.home() / ".config/draft/"

    def load(self):
        raise NotImplementedError
