# bug fix
import collections.abc
from pathlib import Path

from draft.common.Exercise import Exercise
from draft.common.Folder import Folder
from draft.common.helpers import create_list
from draft.common.Prompt import Checkbox, Confirm, Input
from draft.common.Prompter import Prompter

collections.Mapping = collections.abc.Mapping  # type: ignore
from PyInquirer import prompt
from rich import print

from draft.common.Header import Header
from draft.common.Preamble import Preamble
from draft.configuration.Configuration import Configuration
from draft.new.Validators import DocumentNameValidator, ExerciseCountValidator


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
    def document(self) -> str:
        return self._document

    @document.setter
    def document(self, newValue: str):
        self._document = newValue

    @property
    def prompter(self) -> Prompter:
        return self._prompter

    def __init__(self, configuration: Configuration):
        self._configuration = configuration
        self._preamble = Preamble(self.configuration.preamble, self.configuration)
        self._header = Header(
            self.configuration.headers
            / (
                configuration["header"]
                if configuration["header"].endswith(".tex")
                else configuration["header"] + ".tex"
            ),
            self.configuration,
        )
        self._document = ""
        self._prompter = Prompter(configuration)

    def compile(self):
        print(self.configuration)
        self.resolve_draft_exercises()
        print(self.configuration)

    def ask_for_count(self, name: str) -> int:
        """
        Ask how many instances of the exercise should be included.

        Defaults to 1 if `multiple_exercises` is `False`.
        """
        if self.configuration.get("multiple-exercises", False):
            return prompt(
                Input(
                    name="count",
                    message="How many %s should be included?" % name,
                    validate=ExerciseCountValidator,
                )
            ).get("count", 1)
        else:
            return 1

    def resolve_draft_exercises(self):
        """
        Asks which and how many exercises should be included.

        #TODO: placeholders should be scoped per exercise, header, preamble by default

        Accepted format in `draftrc` files:

        ```YAML
        draft-exercises: intervals

        draft-exercises:
            - intervals
            - chords: 2

        draft-exercises:
            - intervals: 3
            - chords:
                count: 2

        draft-exercises:
            intervals: 3

        draft-exercises:
            intervals:
                count: 3
        ```
        """

        result = {}

        # draft-exercises exists in configuration
        if "draft-exercises" in self.configuration:
            draft_exercises = self.configuration["draft-exercises"]

            """
            draft-exercises: intervals
            """
            if (not isinstance(draft_exercises, list)) and (
                not isinstance(draft_exercises, dict)
            ):
                result[draft_exercises] = {"count": self.ask_for_count(draft_exercises)}

            """
            draft-exercises:
                - intervals
            """
            if isinstance(draft_exercises, list):
                for element in draft_exercises:
                    if isinstance(element, dict):
                        for name, count in element.items():
                            print(name, count)
        self.configuration["draft-exercises"] = result

    def _compile(self):
        """
        Compile the document. This involves the following steps:

        1. What should the compiled document be called?
        2. Resolve any prompts in the preamble. Then add its contents to
           `self.document`.
        3. Resolve any prompts in the header.
        4. Compile the exercises.
        """
        # Ask for the name of the compiled document.
        question = Input(
            name="document-name",
            message="What should the compiled document be called?",
            when=lambda a: "document-name" not in self.configuration,
            default=self.header.name,
            validate=DocumentNameValidator,
        )
        self.prompter.ask(question)

        # Process the preamble
        self.prompter.ask(self.preamble.prompts)
        self.preamble.set_placeholders()
        if len(self.preamble.placeholders) != 0:
            raise Exception("Unexpectly found leftover placerholders...")
        self.document += self.preamble.contents

        # Process the header
        self.prompter.ask(self.header.prompts)

        # Ask which exercises to include
        exercises = [
            Exercise(path, self.configuration)
            for path in Folder(self.configuration.exercises).subfiles
            if path.suffix == ".tex"
        ]
        self.prompter.ask(
            Checkbox(
                "draft-exercises",
                [Checkbox.Choice(name=exercise.name) for exercise in exercises],
                "Which exercises should be included?",
                when=lambda _: "draft-exercises" not in self.configuration,
            )
        )

        # prompt about multiple exercises if value hasn't been set
        # in configuration
        self.prompter.ask(
            Confirm(
                "multiple-exercises",
                "Do you want to include any exercise more than once?",
                default=False,
                when=lambda _: "multiple-exercises" not in self.configuration,
            )
        )

        # Clean up data around multiple-dictionaries
        if self.configuration.get("multiple-exercises", False):
            if isinstance(self.configuration["draft-exercises"], dict):
                invalid_keys = []
                for key, value in self.configuration["draft-exercises"].items():
                    try:
                        count = int(value)
                        if count < 1:
                            invalid_keys.append(key)
                    except:
                        invalid_keys.append(key)
                for key in invalid_keys:
                    self.configuration["draft-exercises"].pop(key)
                    # TODO: print warning...
            else:
                draft_exercises = create_list(
                    self.configuration.get("draft-exercises", [])
                )
                answers = {}
                for exercise in draft_exercises:
                    if isinstance(exercise, dict):
                        try:
                            for key, value in exercise.items():
                                count = int(value)
                                if count > 0:
                                    answers[key] = count
                        except:
                            pass
                            # TODO: print a warning
                    else:
                        answer = prompt(
                            questions=Input(
                                exercise,
                                "How many '%s'?" % exercise,
                                validate=ExerciseCountValidator,
                            )
                        )
                        if exercise in answer:
                            answers[exercise] = int(answer[exercise])
                self.configuration["draft-exercises"] = answers
        else:
            # Set each exercise count to 1
            answers = {}
            for exercise in create_list(self.configuration["draft-exercises"]):
                if isinstance(exercise, dict):
                    for key in exercise:
                        answers[key] = 1
                else:
                    answers[exercise] = 1
            self.configuration["draft-exercises"] = answers

        # draft-exercises: {<exercise>: <count>, ...}
        for name, count in self.configuration["draft-exercises"].items():
            print(name, count)
            exercise = Exercise(
                Path(self.configuration.main.parent / "exercises/" / (name + ".tex")),
                self.configuration,
            )
            for i in range(1, count + 1):
                print(
                    "=> Compiling [bold blue]%s[/bold blue]" % exercise.name
                    + ("-%d" % i)
                    if count > 1
                    else ""
                )
                self.prompter.ask(exercise.prompts)

                # remove any unique values
                for unique_placeholder in create_list(
                    exercise.yaml.get("unique-placeholders", [])
                ):
                    self.configuration.pop(unique_placeholder)

        print(self.configuration)
        # print(self.header.contents)

        # print(self.document)
