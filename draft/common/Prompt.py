import collections.abc
from abc import ABC
from enum import Enum
from typing import Any, Callable, Dict
from typing import List as ListType
from typing import Tuple

from draft.common.Prompt import Answers, Prompt

collections.Mapping = collections.abc.Mapping  # type: ignore
from PyInquirer import Separator, Validator

Answers = Dict[str, Any]


class Prompt(dict, ABC):
    """Dictonary representing a PyInquirer prompt."""

    class Type(Enum):
        list = "list"
        rawlist = "rawlist"
        expand = "expand"
        checkbox = "checkbox"
        confirm = "confirm"
        input = "input"
        password = "password"
        editor = "editor"

    def __init__(
        self,
        type: "Prompt.Type",
        name: str,
        message: str | None = None,
        when: Callable[[Answers], bool] | bool = True,
    ):
        self["type"] = type.name
        self["name"] = name
        self["message"] = (
            message
            if message is not None
            else "Please provide a value for '%s'." % name
        )
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
        when: Callable[[Answers], bool] | bool = True,
        default: int | str | Callable[[Answers], str | int] | None = None,
        filter: Callable[[str], str] | None = None,
    ):
        super().__init__(Prompt.Type.list, name, message, when)

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
        when: Callable[[Answers], bool] | bool = True,
        default: int | Callable[[Answers], int] | None = None,
        filter: Callable[[str], str] | None = None,
    ):
        super().__init__(Prompt.Type.rawlist, name, message, when)

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

    class Choice(dict):
        def __init__(self, name: str, key: str, value: str | None = None):
            self["name"] = name
            self["key"] = key
            if value is not None:
                self["value"] = value

    def __init__(
        self,
        name: str,
        choices: ListType[Choice | Separator],
        message: str | None = None,
        default: str | int | Callable[[Answers], str | int] | None = None,
        when: Callable[[Answers], bool] | Validator | None = None,
    ):
        super().__init__(Prompt.Type.expand, name, message, when)

        self["choices"] = choices

        # Validate default value
        if default is not None:
            match default:
                case int(value):
                    if value < len(choices):
                        self["default"] = value
                case str(value):
                    keys = [
                        choice.get("key", "")
                        for choice in choices
                        if isinstance(choice, Expand.Choice)
                    ]
                    if value in keys:
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
        choices: ListType[Choice | Separator],
        message: str | None = None,
        qmark: str | None = None,
        when: Callable[[Answers], bool] | bool = True,
        filter: Callable[[str], str] | None = None,
        validate: Callable[[Answers], bool | str] | Validator | None = None,
    ):
        super().__init__(Prompt.Type.checkbox, name, message, when)
        self["choices"] = choices
        if qmark is not None:
            self["qmark"] = qmark
        if filter is not None:
            self["filter"] = filter
        if validate is not None:
            self["validate"] = validate
