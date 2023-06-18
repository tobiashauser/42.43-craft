from pathlib import Path
from rich import print
import typer
from typing import List, Set, Dict

from .helpers import fetch_github_directory
from .template import Folder, Template


class Exercises(Folder):
    """
    A class encapsulating the exercises directory in the configuration.
    """

    @property
    def path(self) -> Path:
        return self._path

    def __init__(self, path: Path):
        self._path = path
        self.validate()

        # { 'intervals': {'.ly': Exercise, '.tex': Exercise}}
        exercises: Dict[str, Dict[str, Exercises]] = {}
        for file in self.path.iterdir():
            try:
                exercises.append(Exercises(file))
                exercises[file.stem][file.suffix] = Exercises(file)
            except:
                pass
        self.exercises = exercises

#         file_names: Set[str] = {
#             file.name for file in self.path.iterdir() if
#             file.is_file() and (file.suffix == '.tex' or file.suffix == '.ly')
#         }
#
#         exercises: List[Exercise] = []
#         for name in file_names:
#             try:
#                 exercises.append(Exercise(self.path, name))
#             except:
#                 pass
#         self.exercises = exercises

    def validate(self):
        # directory exists
        if not self.path.is_dir():
            self.path.mkdir(parents=True, exist_ok=True)

        # directory is not empty
        if not any(self.path.iterdir()):
            typer.confirm(
                "Do you want to fetch the exercise templates from GitHub?",
                abort=True
            )
            documents = fetch_github_directory(
                'tobiashauser',
                '42.43-draft',
                'templates/exercises'
            )
            for name, contents in documents.items():
                with (self.path / name).open('w') as file:
                    file.write(contents)


class Exercise(Template):
    """
    A class representing one exercise file in the templates' directory.
    """

    @property
    def path(self) -> Path:
        return self._path

    def __init__(self, path: Path):
        self._path = path
        self.validate()
