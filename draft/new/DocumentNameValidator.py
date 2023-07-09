from pathlib import Path
from typing import Optional

from PyInquirer import ValidationError, Validator


class DocumentNameValidator(Validator):
    @staticmethod
    def __validate__(text: str) -> Optional[ValidationError]:
        if not len(text) != 0:
            return ValidationError(
                message="The name of the file cannot be empty.",
                cursor_position=len(text),
            )
        path = Path(text if text.endswith(".tex") else text + ".tex")
        if path.exists():
            return ValidationError(
                message="A document with this name already exists.",
                cursor_position=len(text),
            )

    def validate(self, document):
        error = DocumentNameValidator.__validate__(document.text)
        if error is not None:
            raise error
