import collections.abc
from typing import Callable

from craft_documents.Prompter.Prompt import Answers, Prompt

# Patch bug, caused by change in the collections package since python 3.10 (?)
collections.Mapping = collections.abc.Mapping  # type: ignore
from PyInquirer import Separator


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
        choices: list[Choice] | list[Choice | Separator],
        message: str | None = None,
        default: str | int | Callable[[Answers], str | int] | None = None,
        when: Callable[[Answers], bool] | bool = True,
    ):
        super().__init__(Prompt.Type.expand, name, message, when)

        self["choices"] = choices

        # Validate default value
        if default is not None:
            match default:
                case int(value):
                    if value in range(0, len(choices)):
                        self["default"] = value
                case str(value):
                    keys = [
                        choice.get("key", "")
                        for choice in choices
                        if isinstance(choice, Expand.Choice)
                    ]
                    if value in keys:
                        self["default"] = value
                # BUG: matching against Callable raises an error
                case _:
                    self["default"] = default

    @property
    def default(self) -> str | int | Callable[[Answers], str | int] | None:
        return self.get("default", None)
