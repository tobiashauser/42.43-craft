import oyaml as yaml
from pathlib import Path
import re
from rich import print
import typer
from typing import List, Dict, Set

from .helpers import fetch_github_directory
from .template import Folder, Template


class Headers(Folder):
    """
    A class encapsulating the headers directory in the configuration.
    """

    @property
    def path(self) -> Path:
        return self._path

    def __init__(self, path: Path):
        self._path = path
        self.validate()

        headers: List[Header] = []
        for file in self.path.iterdir():
            if file.is_file() and file.suffix == '.tex':
                try:
                    headers.append(Header(file))
                except:
                    pass
        self.headers = headers

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


class Header(Template):
    """
    A class representing one header file in the templates' directory.
    """

    @property
    def path(self) -> Path:
        return self._path

    def __init__(self, path: Path):
        self._path = path
        self.validate()
