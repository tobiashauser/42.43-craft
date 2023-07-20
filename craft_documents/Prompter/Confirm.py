import collections.abc
from typing import Callable

from craft_documents.Prompter.Prompt import Answers, Prompt

# Patch bug, caused by change in the collections package since python 3.10 (?)
collections.Mapping = collections.abc.Mapping  # type: ignore
# from PyInquirer import


class Confirm(Prompt):
    """
    A confirmation prompt:
    https://github.com/CITGuru/PyInquirer/blob/master/examples/confirm.py

    Take `type`, `name`, `message`[, `default`] properties.
    `default` is expected to be a boolean if used.
    """

    def __init__(
        self,
        name: str,
        message: str | None = None,
        default: bool | Callable[[Answers], bool] | None = None,
        when: Callable[[Answers], bool] | bool = True,
    ):
        super().__init__(Prompt.Type.confirm, name, message, when)

        if default is not None:
            self["default"] = default
