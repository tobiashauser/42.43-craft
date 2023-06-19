import oyaml as yaml
from pathlib import Path
from rich import print
from typing import List, Dict, Any

from .exercises import ExercisesFolder, Exercise
from .headers import HeadersFolder, Header
from .preamble import Preamble


class Configuration:
    """
    A class representing draft's configuration on the system.

    This class provides access to the templates and validates the
    configuration upon initialization.
    """

    @property
    def user_values(self) -> Dict[str, Any]:
        """
        Dictionary representing all provided settings and values
        in `draftrc` and `.draftrc` files from cwd to root.
        """
        if self._user_values is None:
            self.__fetch_user_values__()
        return self._user_values

    # @user_values.setter
    # def user_values(self, newValue: Dict[str, Any]):
    #     self._user_values = newValue

    @property
    def preamble(self) -> Preamble:
        return self._preamble

    @property
    def path(self) -> Path:
        return self._path

    @property
    def templates_path(self) -> Path:
        return self._templates_path

    @property
    def headers_path(self) -> Path:
        return self.templates_path / "headers/"

    @property
    def exercises_path(self) -> Path:
        return self.templates_path / "exercises/"

    @property
    def preamble_path(self) -> Path:
        return self.templates_path / "preamble.tex"

    @property
    def headers_folder(self) -> HeadersFolder:
        return self._headers_folder

    @property
    def headers(self) -> List[Header]:
        return self.headers_folder.headers

    @property
    def exercises_folder(self) -> ExercisesFolder:
        return self._exercises_folder

    @property
    def exercises(self) -> Dict[str, Exercise]:
        return self.exercises_folder.exercises

    def __init__(self):
        # Initialize the underlying storage
        self._user_values = None

        # Path.home() / ".config/draft/"
        self._path: Path = Path("")
        self._templates_path: Path = self.path / "templates/"
        self.validate()

        self._preamble: Preamble = Preamble(self.preamble_path)

        self._exercises_folder = ExercisesFolder(self.exercises_path)
        self._headers_folder = HeadersFolder(self.headers_path)

    def validate(self):
        if (not self.path.is_dir()) \
                or (not self.templates_path.is_dir()):
            print("Creating configuration's directory at " +
                  "[white bold]%s[/white bold]..." % self.path)
            self.templates.mkdir(parents=True, exist_ok=True)

    def __fetch_user_values__(self):
        """
        Accumulate all 'draftrc' and '.draftrc' YAML-files from the current
        working directory up to the root directory in a dictionary.
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
