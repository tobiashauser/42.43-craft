from abc import ABC
from enum import Enum
from typing import Any, Callable

# type PyInquirer.prompt returns
Answers = dict[str, Any]


class Prompt(dict, ABC):
    """
    Dictonary representing a PyInquirer prompt.

    Use the specific subclasses that represent
    the different types of prompt.
    """

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
        test_value: str = "INPUT",
    ):
        self["type"] = type.name
        self["name"] = name
        self["message"] = (
            message
            if message is not None and message != ""
            else f"Please provide the '{name}'."
        )

        self._test_value = test_value

    # MARK: Convenience accessors

    @property
    def name(self) -> str:
        return self["name"]

    @property
    def message(self) -> str:
        return self["message"]

    @property
    def test_value(self) -> str:
        return self._test_value
