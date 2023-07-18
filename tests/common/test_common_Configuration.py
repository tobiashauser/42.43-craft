from pathlib import Path

from craft_documents.configuration.Configuration import (
    Configuration as LiveConfiguration,
)


class Configuration(LiveConfiguration):
    def __init__(self, main=None, root=None, cwd=None, *args, **kwargs):
        """
        This initializer will ignore any values passed to `main`,
        `root` and `cwd`. Instead it uses values that don't leave
        the environment of this repository.
        """
        self._main = Path("config.draft/draftrc")
        self._root = Path()
        self._cwd = Path("tests/configuration")
        self.update(*args, **kwargs)

        self.validate()


def test_instantiation():
    c = Configuration()

    assert "tokens" in c
