from pathlib import Path
from typing import Any, Dict

from draft.configuration.Configuration import Configuration as LiveConfiguration
from draft.configuration.TokensValidator import TokensValidator


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
    c["draft-exercises"] = "intervals"
    c.validate()

    intervals = Path(
        "/Users/tobiashauser/Binder/40-49 Projects/42 Programmieren/42.43 draft/config.draft/exercises/intervals.tex"
    )

    assert c == {
        "allow_eval": True,
        "preamble": Path(
            "/Users/tobiashauser/Binder/40-49 Projects/42 Programmieren/42.43 draft/config.draft/preambles/default.tex"
        ),
        "remove_comments": False,
        "multiple-exercises": True,
        "draft-exercises": {"intervals": {"count": 1, "path": intervals}},
        TokensValidator().key: TokensValidator().default(),
    }

    assert c.allow_eval == True
    assert c.preamble == Path(
        "/Users/tobiashauser/Binder/40-49 Projects/42 Programmieren/42.43 draft/config.draft/preambles/default.tex"
    )
    assert c.remove_comments == False
    assert c.multiple_exercises == True
    assert c.draft_exercises == {"intervals": {"count": 1, "path": intervals}}
