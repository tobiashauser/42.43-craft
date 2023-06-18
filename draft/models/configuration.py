from pathlib import Path
from rich import print
from typing import List, Dict

from .exercises import Exercises, Exercise
from .headers import Headers, Header
from .preamble import Preamble


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
        self.headers: List[Header] = \
            Headers(self.templates / "headers/").headers
        self.exercises: Dict[str, Dict[str, Exercise]] = \
            Exercises(self.templates / "exercises/").exercises

    def validate(self):
        if (not self.basedir.is_dir()) \
                or (not self.templates.is_dir()):
            print("Creating configuration's directory at " +
                  "[white bold]%s[/white bold]..." % self.basedir)
            self.templates.mkdir(parents=True, exist_ok=True)
