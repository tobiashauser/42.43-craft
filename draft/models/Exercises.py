from pathlib import Path
from rich import print
from typer import Abort
from typing import List, Set, Dict


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
            for name, templates in self.defaults.items():
                for extension, contents in templates.items():
                    with (self.path / (name + extension)).open('w') as file:
                        file.write(contents)

    defaults: Dict[str, Dict[str, str]] = {
        'intervals': {
            '.tex': r"""
\input{../preamble.tex}

\begin{document}
    This is an exercise about intervals.
\end{document}
""",
            '.ly': r"""
% This is a template to create an exercise for intervals.
"""
        }
    }


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
