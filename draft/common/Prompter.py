import collections.abc

from rich import print

from draft.common.helpers import combine_dictionaries
from draft.common.Prompt import Prompt

collections.Mapping = collections.abc.Mapping  # type: ignore
from PyInquirer import prompt


class Prompter:
    """
    Class to manage prompting the user for input.
    The answers are added to the storage passed in.
    """

    @property
    def storage(self) -> dict:
        return self._storage

    def __init__(self, storage: dict):
        self._storage = storage

    def ask(self, prompts: Prompt | list[Prompt]):
        """
        Ask the prompts and add the answers to the configuration.
        """
        questions = prompts if isinstance(prompts, list) else [prompts]

        # BUG: The answers will only be added if the storage is not empty
        if len(self.storage) == 0:
            self.storage["NuoXZl"] = ""

        for question in questions:
            if question["name"] not in self.storage:
                prompt(question, answers=self.storage)

        self.storage.pop("NuoXZl", None)
