from pathlib import Path
from rich import print
from typer import Abort
from .Exercises import Exercises
from .Headers import Headers
from .Preamble import Preamble


class Configuration:
    """
    A class representing draft's configuration on the system.

    This class provides access to the templates and validates the
    configuration upon initialization.
    """

    def __init__(self):
        # Path.home() / ".config/draft/"
        self.basedir: Path = Path("config/draft/")
        self.templates: Path = self.basedir / "templates/"
        self.validate()
        self.preamble: Preamble = Preamble(templates / "preamble.tex")
        self.headers: Headers = Headers(templates / "headers/")
        self.exercises: Exercises = Exercises(templates / "exercises/")

    def validate(self):
        if (not self.basedir.is_dir()) \
                or (not self.templates.is_dir()):
            print("[red]TODO: The configuration doesn't exist yet.[/red]")
            raise Abort()
