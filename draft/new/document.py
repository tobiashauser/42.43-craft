from typing import Dict, Any, Optional, Callable

from ..models.configuration import Configuration
from ..models.headers import Header

# bug fix
import collections.abc
collections.Mapping = collections.abc.Mapping
from PyInquirer import prompt

from prompt_toolkit.validation import Validator, ValidationError


class Document:
    """
    A class representing the document created by draft.
    """

    _exercises = None
    _user_values = None

    @property
    def user_values(self):
        if self._user_values is None:
            self.__prompt_for_user_values__()
        return self._user_values

    @user_values.setter
    def user_values(self, newValue: Dict[str, Any]):
        self._user_values = newValue

    @property
    def exercises(self):
        if self._exercises is None:
            self.__prompt_for_exercises__()
        return self._exercises

    def __init__(self, header: Header, configuration: Configuration):
        self.configuration = configuration
        self.header = header

    def prompt_user(self, prompts: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prompt the user with the provided prompts
        and update `self.user_values`
        accordingly.
        """
        def exists(key: str) -> Callable[Dict[str, Any], bool]:
            def when(answers: Dict[str, Any]) -> bool:
                if key in self.configuration.user_values:
                    return False
                else:
                    return True
            return when

        # Omit any prompts for values already defined in
        questions = prompts.copy()
        for question in questions:
            question['when'] = exists(question['name'])

        result = {}
        answers = prompt(questions)
        for key, value in answers.items():
            result[key] = value
        return result

    def __prompt_for_exercises__(self):
        """
        Prompt the user to choose which exercises should be
        included in the document.
        """
        class AmountValidator(Validator):
            def validate(self, document):
                if document.text.isdigit() \
                        and int(document.text) > 0:
                    return True
                else:
                    raise ValidationError(
                        message='Please input a digit 1 or greater.',
                        cursor_position=len(document.text)
                    )

        result: Dict[str, Any] = {}

        exercise_types = self.prompt_user(
            self.configuration.exercises_prompt
        )['exercises']

        # Manage multiple creation
        wants_multiples = prompt({
            'type': 'confirm',
            'name': 'wants_multiples',
            'message': 'Any exercise more than once?',
            'default': False,
            'when': lambda _: len(exercise_types) != 0,
        })['wants_multiples']

        if wants_multiples:
            for exercise in exercise_types:
                amount = prompt({
                    'type': 'input',
                    'message': "How many '%s'?" % exercise,
                    'name': 'amount',
                    'validate': AmountValidator,
                })['amount']

                for i in range(1, int(amount) + 1):
                    templates = self.configuration.exercises[exercise]
                    result.update({
                        exercise + '-' + str(i): templates.copy()
                    })
        else:
            for exercise in exercise_types:
                result.update({
                    exercise: self.configuration.exercises[exercise]
                })

        self._exercises = result

    def __prompt_for_user_values__(self):
        """
        Prompt for any needed user values and store total in
        self.-user_values.
        """
        self._user_values = self.prompt_user(self.header.prompts)
