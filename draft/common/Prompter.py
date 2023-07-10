import collections.abc
from typing import Any, List

from draft.common.Configuration import Configuration
from draft.common.Prompt import Prompt

collections.Mapping = collections.abc.Mapping  # type: ignore
from PyInquirer import prompt
from rich import print


class Prompter:
    """
    Class to manage prompting the user for input.
    The answers are saved in the global configuration.
    """

    @property
    def configuration(self) -> Configuration:
        return self._configuration

    def __init__(self, configuration: Configuration):
        self._configuration = configuration

    def ask(self, prompts: Prompt | List[Prompt]):
        """
        Ask the prompts and add the answers to the configuration.
        """
        questions = prompts if isinstance(prompts, List) else [prompts]
        # print(questions)
        prompt(questions=questions, answers=self.configuration)
