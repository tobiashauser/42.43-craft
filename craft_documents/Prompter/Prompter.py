# Patch bug, caused by change in the collections package since python 3.10 (?)
import collections.abc
import sys
from enum import Enum
from typing import Any

from craft_documents.Prompter.Prompt import Answers, Prompt

collections.Mapping = collections.abc.Mapping  # type: ignore
import PyInquirer


class Prompter:
    """
    Class to interface with PyInquirer and prompt the user for input.

    The prompter can work in two modes: `strict` and `always` (default).

    - `strict`: The user is only prompted if the requested value doesn't
                yet exist in the provided storage.
    - `always`: The user is always prompted and any existing value(s) in
                the provided storage are overridden.
    """

    class Mode(Enum):
        STRICT = 1
        ALWAYS = 2

    def __init__(
        self,
        mode: Mode = Mode.ALWAYS,
        storage: Answers | None = None,
    ):
        self.mode = mode
        self.storage = storage

        # Overwrite ask endpoint for testing
        if "pytest" in sys.modules:
            self.__ask_io = self.__ask_test

    def ask(self, prompt: Prompt) -> Any:
        # setup local reference to flatten the Optional
        storage = self.storage if self.storage is not None else {}

        # BUG: The answers will only be added if the storage is not empty
        if len(storage) == 0:
            storage["ud7pQBvckGbnUYJ9FXzdkU9OuBPQvq"] = ""

        match self.mode:
            case Prompter.Mode.STRICT:
                if prompt.name not in storage:
                    self.__ask_io(prompt, storage)
            case Prompter.Mode.ALWAYS:
                self.__ask_io(prompt, storage)

        # BUG: Remove added key again
        storage.pop("ud7pQBvckGbnUYJ9FXzdkU9OuBPQvq", None)

        # Handle cancellation of prompt with `ctrl-C`
        if prompt.name not in storage:  # never true in testing
            # TODO: Provide a message to the user?
            exit(1)

        return storage[prompt.name]

    def __ask_io(self, prompt: Prompt, storage: Answers):
        PyInquirer.prompt(questions=prompt, answers=storage)

    def __ask_test(self, prompt: Prompt, storage: Answers) -> Any:
        storage[prompt.name] = prompt.test_value
        return prompt.test_value
