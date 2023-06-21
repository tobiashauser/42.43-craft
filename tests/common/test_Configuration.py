from pathlib import Path

from draft.common.Configuration import Configuration as LiveConfiguration


class Configuration(LiveConfiguration):
    def load(self):
        self._path = Path("configuration")


def test_instantiation_and_loading():
    input = Configuration()

    assert input.path == Path.home() / ".config/draft/"
    input.load()
    assert input.path == Path("configuration")
