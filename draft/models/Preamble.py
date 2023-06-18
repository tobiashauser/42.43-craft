from pathlib import Path
from rich import print
from typer import Abort


class Preamble:
    """
    A representing the preamble of the generated document.

    This class provides methods to mutate the preamble.
    """

    def __init__(self, path: Path):
        self.path = path
        self.validate()

    def validate(self):
        # - path is file
        # - file is not empty
        if (not self.path.is_file()) \
                or self.path.stat().st_size == 0:
            print("[red]TODO: Faulty preamble.[/red]")
            raise Abort()

    def load(self):
        """
        Load the preamble from disk.
        """
        with self.path.open('r') as file:
            self.contents = file.read()

    # The default preamble
    default: str = r"""
    \documentclass{scrreport}
    """
