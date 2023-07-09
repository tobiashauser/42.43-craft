import collections.abc

from draft.common.Configuration import Configuration

collections.Mapping = collections.abc.Mapping  # type: ignore
from PyInquirer import prompt


class Prompter:
    """
    Class to manage prompting the user for input.
    The answers are saved in the global configuration.
    """

    @property
    def configuration(self) -> Configuration:
        return self._configuration

    def __init__(self, confiugration: Configuration):
        self._configuration = confiugration

    # def create_prompts
