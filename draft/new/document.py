from typing import Dict, Any, Optional, Callable

from ..models.configuration import Configuration
from ..models.headers import Header

# bug fix
import collections.abc
collections.Mapping = collections.abc.Mapping
from PyInquirer import prompt


class Document:
    """
    A class representing the document created by draft.
    """

    @property
    def user_values(self):
        return self.configuration.user_values

    @user_values.setter
    def user_values(self, newValue: Dict[str, Any]):
        self.configuration.user_values = newValue

    def __init__(self, header: Header, configuration: Configuration):
        self.configuration = configuration
        self.header = header

    def prompt_user(self, prompts: Dict[str, Any]):
        """
        Prompt the user with the provided prompts
        and update `self.configuration.user_values`
        accordingly.
        """
        def exists(key: str) -> Callable[Dict[str, Any], bool]:
            def when(answers: Dict[str, Any]) -> bool:
                if key in self.user_values:
                    return False
                else:
                    return True
            return when

        # Omit any prompts for values already defined in
        questions = prompts.copy()
        for question in questions:
            question['when'] = exists(question['name'])

        answers = prompt(questions)
        for key, value in answers.items():
            self.user_values[key] = value
