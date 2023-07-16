from pathlib import Path

from draft.configuration.Configuration import Configuration as LiveConfiguration


class Configuration(LiveConfiguration):
    def __init__(self, *args, **kwargs):
        self._main = Path("config.draft/draftrc")
        self._root = Path()
        self._cwd = Path("tests/configuration")
        self.update(*args, **kwargs)

        self.validate()


def test_instantiation():
    c = Configuration()

    assert "tokens" in c
