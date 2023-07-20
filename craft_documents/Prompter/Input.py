import collections.abc
from typing import Callable, TypeVar

from craft_documents.Prompter.Prompt import Answers, Prompt

# Patch bug, caused by change in the collections package since python 3.10 (?)
collections.Mapping = collections.abc.Mapping  # type: ignore
from PyInquirer import Validator


class Input(Prompt):
    """
    An input prompt:
    https://github.com/CITGuru/PyInquirer/blob/master/examples/input.py

    Take `type`, `name`, `message`[, `default`, `filter`, `validate`] properties.
    """

    def __init__(
        self,
        name: str,
        message: str | None = None,
        default: str | Callable[[Answers], str] | None = None,
        filter: Callable[[str], str] | None = None,
        when: Callable[[Answers], bool] | bool = True,
        validate: Callable[[str], bool | str] | Validator | None = None,
    ):
        super().__init__(Prompt.Type.input, name, message, when)

        if default is not None:
            self["default"] = default
        if filter is not None:
            self["filter"] = filter
        if validate is not None:
            self["validate"] = validate
