import collections.abc
from typing import Callable

from craft_documents.Prompter.Prompt import Answers, Prompt

# Patch bug, caused by change in the collections package since python 3.10 (?)
collections.Mapping = collections.abc.Mapping  # type: ignore
from PyInquirer import Separator, Validator


class Checkbox(Prompt):
    """
    A checkbox prompt:
    https://github.com/CITGuru/PyInquirer/blob/master/examples/checkbox.py

    Take `type`, `name`, `message`, `choices`[, `qmark`, `filter`, `validate`] properties.

    Choices marked as {'checked': True} will be checked by default.

    Choices whose property `disabled` is True will be unselectable.
    If `disabled` is a string, then the string will be outputted next
    to the disabled choice, otherwise it'll default to "Disabled".
    The disabled property can also be a synchronous function
    receiving the current answers as argument and returning a boolean
    or a string.

    The `pointer_index` kwarg can be used to specify initial pointer position.
    """

    class Choice(dict):
        def __init__(
            self,
            name: str,
            value: str | None = None,
            checked: bool | None = None,
            disabled: bool | str | Callable[[Answers], bool | str] | None = None,
        ):
            self["name"] = name
            if value is not None:
                self["value"] = value
            if checked is not None:
                self["checked"] = checked
            if disabled is not None:
                self["disable"] = disabled

    def __init__(
        self,
        name: str,
        choices: list[Choice | Separator],
        message: str | None = None,
        qmark: str | None = None,
        when: Callable[[Answers], bool] | bool = True,
        filter: Callable[[str], str] | None = None,
        validate: Callable[[str], bool | str] | Validator | None = None,
    ):
        super().__init__(Prompt.Type.checkbox, name, message, when)
        self["choices"] = choices
        if qmark is not None:
            self["qmark"] = qmark
        if filter is not None:
            self["filter"] = filter
        if validate is not None:
            self["validate"] = validate
