from pathlib import Path

from draft.common.Configuration import Configuration as LiveConfiguration


class Configuration(LiveConfiguration):
    def load(self):
        # override live path
        self._path = Path("configuration")


def test_instantiation_and_loading():
    input = Configuration()

    assert input.path == Path("configuration")
