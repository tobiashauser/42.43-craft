from pathlib import Path
import typer
from typing import Dict, Any

from .helpers import fetch_github_directory
from .template import Folder, Template


class Exercises(Folder):
    """
    A class encapsulating the exercises directory in the configuration.
    """

    _prompts = None

    @property
    def path(self) -> Path:
        return self._path

    @property
    def prompts(self) -> Dict[str, Any]:
        if self._prompts is None:
            self.__create_prompts__()
        return self._prompts

    def __init__(self, path: Path):
        self._path = path
        self.validate()

        # { 'intervals': {'.ly': Exercise, '.tex': Exercise}}
        exercises: Dict[str, Dict[str, Exercises]] = {}
        for file in self.path.iterdir():
            # exercises[file.stem][file.suffix] = Exercise(file)
            if file.stem in exercises:
                exercises[file.stem][file.suffix] = Exercise(file)
            else:
                exercises.update({file.stem: {file.suffix: Exercise(file)}})
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

    def __create_prompts__(self):
        """
        Create the prompt to choose from all exercise templates.
        """
        question = {
            'type': 'checkbox',
            'message': 'Which exercises should be included?',
            'name': 'exercises',
            'choices': [{'name': exercise} for exercise in self.exercises.keys()]
        }
        self._prompts = [question]


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
