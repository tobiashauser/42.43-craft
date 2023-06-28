from pathlib import Path
from typing import List

import oyaml as yaml


class Configuration(dict):
    """
    A dictionary like class that represents the
    configuration of the user.

    Special keys:
    - `allow_eval`: If true, the user can specify lambdas to
        customize how prompts behave. This is opt in because
        it opens up security issues.
    - `draft-exercises`: Holds a list of exercises to be
        included in the compiled document.
        (also "Special placeholders")
    - `remove_comments`: If true, comments from the templates
        will be removed when compiling the document.

    Special placeholders:
    - `<<draft-exercises>>`: This placeholder gets replaced by
        the exericses. It should only appear in a header.
        It can also be set in a `draftrc` configuration file.
    """

    @property
    def root(self) -> Path:
        return self._root

    @property
    def cwd(self) -> Path:
        return self._cwd

    def __init__(
        self, root: Path = Path.home(), cwd: Path = Path.cwd(), *args, **kwargs
    ):
        self._root = root
        self._cwd = cwd
        self.update(*args, **kwargs)
        self.load()

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
