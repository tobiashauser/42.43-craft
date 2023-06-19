from pathlib import Path
import typer
from typing import Dict, Any

from .helpers import fetch_github_directory
from .base_classes.folder import Folder
from .base_classes.template import Template


class ExerciseTemplate(Template):
    """
    A class representing one exercise file in the templates' directory.
    """

    @property
    def path(self) -> Path:
        return self._path

    def __init__(self, path: Path):
        super().__init__()
        self._path = path
        self.validate()


class Exercise:
    r"""
    A class representing one exercise type.

    An exercise consists of one main template (intervals.tex) whose
    contents are written into the compiled document.

    Furthermore it can have supplemental files (with different endings)
    which are copied (and renamed if multiple exercises of this type are
    needed) to the current working directory.

    Draft defines a special placeholder `<<exercise-name>>` which can be used
    to include any supplemental files into the compiled document:

    ```tex
    \begin{document}
        \lilypondfile{<<exercise-name>>.ly}
    \end{document}
    ```
    """

    @property
    def name(self) -> str:
        return self._name

    @property
    def tex(self) -> ExerciseTemplate:
        return self._tex_template

    @property
    def supplements(self) -> Dict[str, ExerciseTemplate]:
        return self._supplements

    def __init__(self, path: Path, stem: str):
        self._name = stem

        # initialize supplements and tex
        supplements: Dict[str, ExerciseTemplate] = {}
        for file in path.iterdir():
            if file.stem != stem:  # not very efficient
                continue
            if file.suffix == '.tex':
                self._tex_template = ExerciseTemplate(file)
            else:
                supplements[file.suffix] = ExerciseTemplate(file)
        self._supplements = supplements


class ExercisesFolder(Folder):
    """
    A class encapsulating the exercises directory in the configuration.
    """

    @property
    def path(self) -> Path:
        return self._path

    @property
    def prompt(self) -> Dict[str, Any]:
        if self._prompts is None:
            self.__create_prompt__()
        return self._prompt

    @property
    def exercises(self) -> Dict[str, Exercise]:
        if self._exercises is None:
            self.__init_exercises__()
        return self._exercises

    def __init__(self, path: Path):
        # Initialize the underlying storage
        self._prompt = None
        self._path = path
        self._exercises = None

        self.validate()

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

    def __create_prompt__(self):
        """
        Create the prompt to choose from all exercise templates.
        """
        question = {
            'type': 'checkbox',
            'message': 'Which exercises should be included?',
            'name': 'exercises',
            'choices': [{'name': exercise.name} for exercise in self.exercises]
        }
        self._prompt = [question]

    def __init_exercises__(self):
        exercises: Dict[str, Exercise] = {}
        for file in self.path.iterdir():
            exercises[file.stem] = Exercise(self.path, file.stem)
        self._exercises = exercises
