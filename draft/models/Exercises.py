from pathlib import Path
from rich import print
from typer import Abort
from typing import List, Set, Optional


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
        for name in file_names():
            try:
                exercises.append(Exercise(self.path, name))
            except _:
                pass
        self.exercises = exercises

    def validate(self):
        # - directory exists
        # - is not empty
        if (not self.path.is_dir()) \
                or any(self.path.iterdir()):
            print("[red]TODO: Faulty headers directory.[/red]")
            raise Abort()


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
            raise Abort()

        if (not self.ly_path.is_file()) \
                or self.ly_path.stat().st_size == 0:
            print("[red]TODO: Faulty tex exercise template.[/red]")
            raise Abort()

    def load(self):
        """
        Load the contents of the templates from the disk.
        """
        with self.tex_path.open('r') as file:
            self.tex_template = file.read()

        with self.ly_path.open('r') as file:
            self.ly_template = file.read()
