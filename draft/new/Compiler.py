import collections.abc

from rich import print

collections.Mapping = collections.abc.Mapping  # type: ignore
from PyInquirer import prompt  # bugfix collections

from draft.common.Exercise import Exercise
from draft.common.Folder import Folder
from draft.common.Header import Header
from draft.common.Preamble import Preamble
from draft.common.Prompt import Checkbox, Input
from draft.common.TemplateManager import TemplateManager
from draft.configuration.Configuration import Configuration
from draft.configuration.DraftExercisesValidator import (
    DraftExercisesValidator,
    ExerciseConfiguration,
)
from draft.configuration.MultipleExercisesValidator import MultipleExercisesValidator
from draft.new.Validators import ExerciseCountValidator


class Compiler:
    """
    Class that handles compiling a document.
    """

    @property
    def configuration(self) -> Configuration:
        return self._configuration

    @property
    def preamble(self) -> Preamble:
        return self._preamble

    @property
    def header(self) -> Header:
        return self._header

    @property
    def exercises(self) -> list[Exercise]:
        """
        The exercises to be included in the compiled document.
        The order cannot be guaranteed.
        """
        return self._exercises

    @property
    def template_manager(self) -> TemplateManager:
        return self._template_manager

    def __init__(self, configuration: Configuration):
        """
        You should guarantee values for `preamble` and `header` in the
        configuration when creating an instance of a Compiler.
        """

        self._configuration = configuration
        self._preamble = Preamble(configuration.preamble, configuration)
        self._template_manager = TemplateManager(self.configuration)

        if configuration.header is not None:
            self._header = Header(configuration.header, configuration)
        else:
            raise Exception("Unexpectedly found `None` at `configuration.header`.")
            # TODO: Handle Exception

        # Prompt for exercises if they are not defined in a configuration file
        if DraftExercisesValidator().key not in self.configuration:
            self.configuration[
                DraftExercisesValidator().key
            ] = self.prompt_for_exercises()

        self._exercises: list[Exercise] = []
        for config in self.configuration[DraftExercisesValidator().key].values():
            self._exercises += [
                Exercise(config["path"], self.configuration)
                for _ in range(config["count"])
            ]

    def compile(self):
        """
        Compile the document.
        """
        print(self.configuration)

    def prompt_for_exercises(self) -> dict:
        """
        Prompt the user which exercises should be included.
        """
        key = DraftExercisesValidator().key
        question = Checkbox(
            DraftExercisesValidator().key,
            [
                Checkbox.Choice(name=exercise.name)
                for exercise in self.template_manager.exercises
            ],
            "Which exercises should be included?",
            when=lambda _: key not in self.configuration,
        )

        # answer = ['intervals']
        answer = prompt(question)[key]
        answer = {
            exercise_name: ExerciseConfiguration(self.configuration, exercise_name)
            for exercise_name in answer
        }
        # answer = {'intervals': {'count': ..., 'path': ... }}

        # multiple exercises
        if self.configuration[MultipleExercisesValidator().key]:
            for exercise_name, config in answer.items():
                question = Input(
                    "count",
                    message="How many '%s'?" % exercise_name,
                    default=str(config["count"]),
                    validate=ExerciseCountValidator,
                )
                count = prompt(question)["count"]
                config["count"] = int(count)

        return answer
