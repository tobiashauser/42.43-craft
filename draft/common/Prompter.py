import collections.abc

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
        prompt(questions=questions, answers=self.storage)
