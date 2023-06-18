from pathlib import Path
import typer

from .helpers import fetch_github_document
from .template import Template


class Preamble(Template):
    """
    A representing the preamble of the generated document.

    This class provides methods to mutate the preamble.
    """

    @property
    def path(self) -> str:
        return self._path

    def __init__(self, path: Path):
        self._path = path
        self.validate()

    def validate(self):
        # - path is file
        # - file is not empty
        if (not self.path.is_file()) \
                or self.path.stat().st_size == 0:
            typer.confirm(
                "Do you want to fetch the header templates from GitHub?",
                abort=True
            )
            name, contents = fetch_github_document(
                'tobiashauser',
                '42.43-draft',
                'templates/preamble.tex'
            )
            with (self.path).open('w') as file:
                file.write(contents)
