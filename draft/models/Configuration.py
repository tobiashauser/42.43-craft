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
        self.basedir: Path = Path("")
        self.templates: Path = self.basedir / "templates/"
        self.validate()
        self.preamble: Preamble = Preamble(self.templates / "preamble.tex")
        self.headers: Headers = Headers(self.templates / "headers/")
        self.exercises: Exercises = Exercises(self.templates / "exercises/")

    def validate(self):
        if (not self.basedir.is_dir()) \
                or (not self.templates.is_dir()):
            print("Creating configuration's directory at " +
                  "[white bold]%s[/white bold]..." % self.basedir)
            self.templates.mkdir(parents=True, exist_ok=True)
