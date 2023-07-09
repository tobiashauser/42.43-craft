import collections.abc
from abc import ABC
from enum import Enum
from typing import Any, Callable, Dict
from typing import List as ListType
from typing import Tuple

collections.Mapping = collections.abc.Mapping  # type: ignore
from PyInquirer import Separator, Validator

Answers = Dict[str, Any]


class PromptType(Enum):
    list = "list"
    rawlist = "rawlist"
    expand = "expand"
    checkbox = "checkbox"
    confirm = "confirm"
    input = "input"
    password = "password"
    editor = "editor"


class Prompt(dict, ABC):
    """Dictonary representing a PyInquirer prompt."""

    def __init__(
        self,
        type: PromptType,
        name: str,
        message: str | None = None,
        when: Callable[[Answers], bool] | Validator | None = None,
    ):
        self["type"] = type.name
        self["name"] = name
        self["message"] = (
            message
            if message is not None
            else "Please provide a value for '%s'." % name
        )
        if when is not None:
            self["when"] = when


class List(Prompt):
    """
    A list prompt:
    https://github.com/CITGuru/PyInquirer/blob/master/examples/list.py

    Take `type`, `name`, `message`, `choices`[, `default`, `filter`] properties.
    (Note that default must be the choice index in the array or a choice value.)
    """

    def __init__(
        self,
        name: str,
        choices: ListType[str | Separator],
        message: str | None = None,
        when: Callable[[Answers], bool] | Validator | None = None,
        default: int | str | Callable[[Answers], str | int] | None = None,
        filter: Callable[[str], str] | Callable[[Answers], str] | None = None,
    ):
        super().__init__(PromptType.list, name, message, when)

        self["choices"] = choices

        if filter is not None:
            self["filter"] = filter

        # Validate default value
        if default is not None:
            match default:
                case int(value):
                    if value < len(choices):
                        self["default"] = value
                case str(value):
                    if value in choices:
                        self["default"] = value
                case _:
                    self["default"] = default


class RawList(Prompt):
    """
    A rawlist prompt:
    https://github.com/CITGuru/PyInquirer/blob/master/examples/rawlist.py

    Take `type`, `name`, `message`, `choices`[, `default`, `filter`] properties.
    (Note that default must the choice index in the array.)
    """

    def __init__(
        self,
        name: str,
        choices: ListType[str | Separator],
        message: str | None = None,
        when: Callable[[Answers], bool] | Validator | None = None,
        default: int | Callable[[Answers], int] | None = None,
        filter: Callable[[str], str] | Callable[[Answers], str] | None = None,
    ):
        super().__init__(PromptType.rawlist, name, message, when)

        self["choices"] = choices

        if filter is not None:
            self["filter"] = filter

        # Validate default value
        if default is not None:
            match default:
                case int(value):
                    if value < len(choices):
                        self["default"] = value
                case _:
                    self["default"] = default


class Expand(Prompt):
    """
    An expand prompt:
    https://github.com/CITGuru/PyInquirer/blob/master/examples/expand.py

    Take `type`, `name`, `message`, `choices`[, `default`] properties.
    (Note that default must be the choice index in the array or a key.
    If default key not provided, then help will be used as default choice.)

    Note that the choices object will take an extra parameter
    called key for the expand prompt. This parameter must be a
    single (lowercased) character. The `h` option is added by the
    prompt and shouldn't be defined by the user.
    """

    class Choice:
        def __init__(self, name: str, key: str, value: str):
            self.name = name
            self.key = key
            self.value = value

    def __init__(
        self,
        name: str,
        choices: ListType[Choice | Separator],
        message: str | None = None,
        default: str | int | Callable[[Answers], str | int] | None = None,
        when: Callable[[Answers], bool] | Validator | None = None,
    ):
        super().__init__(PromptType.expand, name, message, when)

        self["choices"] = choices

        # Validate default value
        if default is not None:
            match default:
                case int(value):
                    if value < len(choices):
                        self["default"] = value
                case str(value):
                    for e in choices:
                        if isinstance(e, Choice):
                            if e.key == value:
                                self["default"] = value
                case _:
                    self["default"] = default


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
