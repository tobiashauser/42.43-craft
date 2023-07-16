from pathlib import Path
from typing import Any, Dict

from draft.configuration.Configuration import Configuration as LiveConfiguration


class Configuration(LiveConfiguration):
    """
    This class can be used for testing.
    It doesn't set any values by itself.
    """

    def __init__(self, *args, **kwargs):
        self._main = Path("config.draft/draftrc")
        self._root = Path()
        self._cwd = Path("tests/configuration")
        self.update(*args, **kwargs)


def test_instantiation():
    c = Configuration()
    assert c == {}


def test_properties_after_validate():
    c = Configuration(allow_eval=True)
    c.validate()

    assert c == {
        "allow_eval": True,
        "preamble": Path(
            "/Users/tobiashauser/Binder/40-49 Projects/42 Programmieren/42.43 draft/config.draft/preambles/default.tex"
        ),
        "remove_comments": False,
        "multiple-exercises": True,
    }

    assert c.allow_eval == True
    assert c.preamble == Path(
        "/Users/tobiashauser/Binder/40-49 Projects/42 Programmieren/42.43 draft/config.draft/preambles/default.tex"
    )
    assert c.remove_comments == False
    assert c.multiple_exercises == True
