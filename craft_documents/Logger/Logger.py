import sys
from io import StringIO
from typing import IO, Any

from rich import print as rprint

from craft_documents.Logger.History import History


class Logger:
    """
    A class to control logging events that happen during the
    execution of a programm or script.

    Loosely modelled after: https://docs.python.org/3/howto/logging.html.

    The class has different methods corresponding to different semantic
    connotations of logging, such as `console` to print to the console or
    `debug` (#TODO) to provide debug information.

    Additionally every event is stored in `Logger.history`. This allows
    exhaustive testing of what happened. `Logger.history` can be filtered
    by the semantic of the events.
    """

    def __init__(self):
        self.history = History()

        # Overwrite endpoints for testing
        if "pytest" in sys.modules:
            self.__console_io = self.__console_test

    def __print_string(
        self,
        *objects: Any,
        sep: str = " ",
        end: str = "\n",
        file: IO[str] | None = None,
        flush: bool = False
    ) -> str:
        s = StringIO()
        print(*objects, sep, end, s, flush)
        return s.getvalue()

    # MARK: Console

    def console(
        self,
        *objects: Any,
        sep: str = " ",
        end: str = "\n",
        file: IO[str] | None = None,
        flush: bool = False
    ):
        """
        Print a message to the console.

        This method mirrors the API used by python's `print` and
        can be used in the exact same way. However, it uses
        `rich.print` to allow styling of the   output.
        """
        # Save to history
        result = self.__print_string(*objects, sep, end, file, flush)
        self.history.add(History.Event.Semantic.CONSOLE, result)

        self.__console_io(*objects, sep, end, file, flush)

    def __console_io(
        self,
        *objects: Any,
        sep: str = " ",
        end: str = "\n",
        file: IO[str] | None = None,
        flush: bool = False
    ):
        rprint(*objects, sep, end, file, flush)

    def __console_test(
        self,
        *objects: Any,
        sep: str = " ",
        end: str = "\n",
        file: IO[str] | None = None,
        flush: bool = False
    ):
        pass
