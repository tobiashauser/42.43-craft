import oyaml as yaml
from pathlib import Path
from rich import print
from typing import List, Dict, Any

from .exercises import Exercises, Exercise
from .headers import Headers, Header
from .preamble import Preamble


class Configuration:
    """
    A class representing draft's configuration on the system.

    This class provides access to the templates and validates the
    configuration upon initialization.
    """

    _user_values = None

    @property
    def user_values(self) -> Dict[str, Any]:
        if self._user_values is None:
            self.__fetch_user_values__()
        return self._user_values

    @user_values.setter
    def user_values(self, newValue: Dict[str, Any]):
        self._user_values = newValue

    def __init__(self):
        # Path.home() / ".config/draft/"
        self.basedir: Path = Path("")
        self.templates: Path = self.basedir / "templates/"
        self.validate()

        self.preamble: Preamble = Preamble(self.templates / "preamble.tex")

        self.headers: List[Header] = \
            Headers(self.templates / "headers/").headers

        exercises = Exercises(self.templates / "exercises/")
        self.exercises: Dict[str, Dict[str, Exercise]] = exercises.exercises
        self.exercises_prompt = exercises.prompts

    def validate(self):
        if (not self.basedir.is_dir()) \
                or (not self.templates.is_dir()):
            print("Creating configuration's directory at " +
                  "[white bold]%s[/white bold]..." % self.basedir)
            self.templates.mkdir(parents=True, exist_ok=True)

    def __fetch_user_values__(self):
        """
        Accumulate all 'draftrc' and '.draftrc' YAML-files from the current
        working directory to the root directory in a dictionary.
        """
        user_values: Dict[str, Any] = {}
        allowed_file_names = ['draftrc', '.draftrc']
        directory = Path.cwd()

        while True:
            for file_name in allowed_file_names:
                file_path = directory / file_name
                if file_path.is_file():
                    data = yaml.safe_load(file_path.open())

                    # Continue with parent if no data could be loaded
                    if data is None:
                        continue

                    # Insert any new values
                    for key, value in data.items():
                        if key not in user_values:
                            user_values[key] = value

            # Exit if the root directory has been reached
            if directory == Path.home():
                break

            # Move up to the parent directory
            directory = directory.parent

        self._user_values = user_values
