from pathlib import Path

from draft.configuration.Semantic import Semantic
from draft.configuration.Validator import Validator


class PreambleValidator(Validator):
    """
    Accepts an absolute or relative path to a tex-file.
    Relative paths will be interpreted as being inside
    `~/.config/draft/preambles/`.

    Defaults to an absolute path to a tex-file.
    """

    def __init__(self):
        self._key = "preamble"
        self._semantic = Semantic.REQUIRED

    def lint(self, value: str) -> Path:
        path = Path(value) if value.endswith(".tex") else Path(value + ".tex")
        if path.is_absolute():
            return path.resolve()
        else:
            return (self.configuration.main.parent / "preambles/" / path).resolve()

    def validate(self, value: str) -> bool:
        path = Path(value)
        if path.is_file():
            return True
        else:
            return False

    def default(self) -> Path:
        """
        Return the default preamble.
        """
        default = "default.tex"

        path = self.configuration.main.parent / ("preambles/" + default)
        if path.is_file():
            return path.resolve()
        else:
            raise Exception("The default preamble file doesn't exist.")
