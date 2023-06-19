from pathlib import Path
import typer
from typing import List

from .helpers import fetch_github_directory
from .base_classes.folder import Folder
from .base_classes.template import Template


class Header(Template):
    """
    A class representing one header file in the templates' directory.
    """

    @property
    def path(self) -> Path:
        return self._path

    def __init__(self, path: Path):
        super().__init__()
        self._path = path
        self.validate()


class HeadersFolder(Folder):
    """
    A class encapsulating the headers directory in the configuration.
    """

    @property
    def path(self) -> Path:
        return self._path

    @property
    def headers(self) -> List[Header]:
        if self._headers is None:
            self.__init_headers__()
        return self._headers

    def __init__(self, path: Path):
        self._path = path
        self._headers = None
        self.validate()

    def validate(self):
        # - directory exists
        if not self.path.is_dir():
            self.path.mkdir(parents=True, exist_ok=True)

        # directory is not empty
        if not any(self.path.iterdir()):
            typer.confirm(
                "Do you want to fetch the header templates from GitHub?",
                abort=True
            )
            documents = fetch_github_directory(
                'tobiashauser',
                '42.43-draft',
                'templates/headers'
            )
            for name, contents in documents.items():
                with (self.path / name).open('w') as file:
                    file.write(contents)

    def __init_headers__(self):
        headers: List[Header] = []
        for file in self.path.iterdir():
            if file.is_file() and file.suffix == '.tex':
                try:
                    headers.append(Header(file))
                except:
                    pass
        self._headers = headers
