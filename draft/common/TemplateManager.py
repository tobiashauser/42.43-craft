from pathlib import Path
from typing import List

from draft.common.Configuration import Configuration
from draft.common.Exercise import Exercise
from draft.common.Folder import Folder
from draft.common.Header import Header
from draft.common.Preamble import Preamble


class TemplateManager:
    """
    A class that manages the templates installed on the system.
    """

    @property
    def folder(self) -> Folder:
        return self._folder

    @property
    def headers(self) -> List[Header]:
        return self._headers

    @property
    def exercises(self) -> List[Exercise]:
        return self._exercises

    def __init__(self, configuration: Configuration):
        self._folder = Folder(configuration.main.parent)
        self._headers = [
            Header(path, configuration)
            for headers in self.folder.subfolders
            for path in Folder(headers).subfiles
            if headers.name == "headers"
            if path.suffix == ".tex"
        ]
        self._exercises = [
            Exercise(path, configuration)
            for exercises in self.folder.subfolders
            for path in Folder(exercises).subfiles
            if exercises.name == "exercises"
            if path.suffix == ".tex"
        ]
