import collections.abc
from typing import Callable

from craft_documents.Prompter.Prompt import Answers, Prompt

# Patch bug, caused by change in the collections package since python 3.10 (?)
collections.Mapping = collections.abc.Mapping  # type: ignore
from PyInquirer import Separator


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
        choices: list[str] | list[str | Separator],
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
                    if value in range(0, len(choices)):
                        self["default"] = value
                # BUG: matching against Callable raises an error
                case _:
                    self["default"] = default

    @property
    def default(self) -> int | Callable[[Answers], int] | None:
        return self.get("default", None)
