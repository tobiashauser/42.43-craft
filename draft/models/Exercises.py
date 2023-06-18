from pathlib import Path
from rich import print
import typer
from typing import List, Set, Dict

from .helpers import fetch_github_directory


class Exercises:
    """
    A class encapsulating the exercises directory in the configuration.
    """

    def __init__(self, path: Path):
        self.path = path
        self.validate()

        file_names: Set[str] = {
            file.name for file in self.path.iterdir() if
            file.is_file() and (file.suffix == '.tex' or file.suffix == '.ly')
        }

        exercises: List[Exercise] = []
        for name in file_names:
            try:
                exercises.append(Exercise(self.path, name))
            except:
                pass
        self.exercises = exercises

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


class Exercise:
    """
    A class representing one exercise file in the templates' directory.
    """

    def __init__(self, directory: Path, name: str):
        self.tex_path = directory / name + '.tex'
        self.ly_path = directory / name + '.ly'
        self.validate()

    def validate(self):
        # - tex and ly templates exist
        # - they are not empty
        if (not self.tex_path.is_file()) \
                or self.tex_path.stat().st_size == 0:
            print("[red]TODO: Faulty tex exercise template.[/red]")
            raise typer.Abort()

        if (not self.ly_path.is_file()) \
                or self.ly_path.stat().st_size == 0:
            print("[red]TODO: Faulty tex exercise template.[/red]")
            raise typer.Abort()

    def load(self):
        """
        Load the contents of the templates from the disk.
        """
        with self.tex_path.open('r') as file:
            self.tex_template = file.read()

        with self.ly_path.open('r') as file:
            self.ly_template = file.read()
