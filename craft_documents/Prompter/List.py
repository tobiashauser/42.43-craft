import collections.abc
from typing import Callable

from craft_documents.Prompter.Prompt import Answers, Prompt

# Patch bug, caused by change in the collections package since python 3.10 (?)
collections.Mapping = collections.abc.Mapping  # type: ignore
from PyInquirer import Separator


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
        choices: list[str] | list[str | Separator],
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
                    if value in range(0, len(choices)):
                        self["default"] = value
                case str(value):
                    if value in choices:
                        self["default"] = value
                # BUG: matching against Callable raises an error
                case _:
                    self["default"] = default

    @property
    def default(self) -> int | str | Callable[[Answers], str | int] | None:
        return self.get("default", None)
