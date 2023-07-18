from __future__ import annotations

from pathlib import Path
from typing import Any, List

import yaml

from draft.configuration.AllowEvalValidator import AllowEvalValidator
from draft.configuration.DocumentNameValidator import DocumentNameValidator
from draft.configuration.DraftExercisesValidator import DraftExercisesValidator
from draft.configuration.HeaderValidator import HeaderValidator
from draft.configuration.MultipleExercisesValidator import MultipleExercisesValidator
from draft.configuration.PreambleValidator import PreambleValidator
from draft.configuration.RemoveCommentsValidator import RemoveCommentsValidator
from draft.configuration.TokensValidator import TokensValidator
from draft.configuration.UniqueExercisePlaceholdersValidator import (
    UniqueExercisePlaceholdersValidator,
)
from draft.configuration.Validator import Validator
from draft.configuration.VerboseValidator import VerboseValidator


class Configuration(dict):
    """
    A dictionary like class that represents the configuration
    of the user.

    ### Settings

    - `preamble`: required, defaults to `default.tex`
    - `allow_eval`: required, defaults to `False`
    - `remove_comments`: required, defaults to `False`
    - `draft-exercises`: optional
    - `multiple-exercises`: required, defaults to `True`
    - `tokens`: required, loads defaults for `.tex` and `.ly`
    """

    @property
    def validators(self) -> list[Validator]:
        return self._validators

    @property
    def main(self) -> Path:
        return self._main

    @property
    def root(self) -> Path:
        return self._root

    @property
    def cwd(self) -> Path:
        return self._cwd

    @property
    def preamble(self) -> Path:
        return self[PreambleValidator().key]

    @property
    def header(self) -> Path | None:
        return self.get(HeaderValidator().key, None)

    @header.setter
    def header(self, name: str | Path):
        """
        Set this property with the name of the header. It can optionally have the suffix
        `.tex`.

        #TODO: Settings with a relative path is not supported.
        """
        v = HeaderValidator()
        old_value = self.header

        self[v.key] = name
        v.run(self)
        if self.header is None:
            self[v.key] = old_value
            if self.header is None:
                self.pop(v.key)

    @property
    def allow_eval(self) -> bool:
        return self[AllowEvalValidator().key]

    @property
    def verbose(self) -> bool:
        return self[VerboseValidator().key]

    @property
    def remove_comments(self) -> bool:
        return self[RemoveCommentsValidator().key]

    @property
    def draft_exercises(self) -> dict[str, dict[str, Any]] | None:
        return self.get(DraftExercisesValidator().key, None)

    @property
    def multiple_exercises(self) -> bool:
        return self[AllowEvalValidator().key]

    @property
    def unique_exercise_placeholders(self) -> bool:
        return self[UniqueExercisePlaceholdersValidator().key]

    @property
    def document_name(self) -> str:
        return self.get(DocumentNameValidator().key, None)

    def __init__(
        self,
        main: Path = Path.home() / ".config/draft/draftrc",
        root: Path = Path.home(),
        cwd: Path = Path.cwd(),
        *args,
        **kwargs,
    ):
        self._main = main
        self._root = root
        self._cwd = cwd

        self.update(*args, **kwargs)
        self.load()
        self.validate()

    def load(self):
        """
        Load the configuration from the disk.

        The user can configure draft in yaml-formatted
        configuration files: `draftrc`, `.draftrc`.

        Draft will read all configuration files from
        the current working directory to home and
        accumulate their values. Files closer to
        the current working directory take
        precedence.

        Additionally there is one configuration file
        at `~/.config/draft/draftrc` which stores
        gets read last. It stores global configuration
        such as prefixes for single-line-comments for
        a specific file extension. Make sure to escape
        them correctly.
        """
        files: List[str] = ["draftrc", ".draftrc"]
        directory: Path = self.cwd

        while True:
            for file in files:
                file_path: Path = directory / file
                if not file_path.is_file():
                    continue
                try:
                    data = yaml.safe_load(file_path.open())
                    # Insert any new values
                    for key, value in data.items():
                        if key not in self:
                            self[key] = value
                except:
                    continue
            # Exit if the root directory has been reached
            if directory == self.root:
                break

            # Move up to the parent directory
            directory = directory.parent

        # read file at `~/.config/draft/draftrc`
        try:
            data = yaml.safe_load(self.main.open())
            for key, value in data.items():
                if key not in self:
                    self[key] = value
        except:
            pass

    def validate(self):
        """
        Validate the configuration and employ resolving strategies if
        necessary. This is done by setting and running every validator in
        `self.validators`.
        """
        self._validators = [
            PreambleValidator(),
            AllowEvalValidator(),
            RemoveCommentsValidator(),
            AllowEvalValidator(),
            DraftExercisesValidator(),
            MultipleExercisesValidator(),
            TokensValidator(),
            HeaderValidator(),
            UniqueExercisePlaceholdersValidator(),
            DocumentNameValidator(),
            VerboseValidator(),
        ]
        for validator in self.validators:
            validator.run(self)
