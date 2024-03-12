from pathlib import Path
from typing import Any, Dict
import pytest

from craft_documents.configuration.Configuration import (
    Configuration as LiveConfiguration,
)
from craft_documents.configuration.TokensValidator import TokensValidator


class Configuration(LiveConfiguration):
    """
    This class can be used for testing.
    It doesn't set any values by itself.
    """

    def __init__(self, *args, **kwargs):
        self._main = Path("config.craft/craftrc")
        self._root = Path()
        self._cwd = Path("tests/configuration")
        self.update(*args, **kwargs)


def test_instantiation():
    c = Configuration()
    assert c == {}


def test_properties_after_validate(request):
    c = Configuration(allow_eval=True)
    c["craft-exercises"] = "intervals"
    c.validate()

    intervals = request.config.rootdir / "config.craft/exercises/intervals.tex"

    assert c == {
        "allow_eval": True,
        "preamble": request.config.rootdir / "config.craft/preambles/default.tex",
        "remove_comments": False,
        "multiple-exercises": True,
        "craft-exercises": {"intervals": {"count": 1, "path": intervals}},
        TokensValidator().key: TokensValidator().default(),
        "unique_exercise_placeholders": False,
        "verbose": False,
    }


def test_header_setter(request):
    exam = Path(request.config.rootdir / "config.craft/headers/exam.tex")
    worksheet = Path(request.config.rootdir / "config.craft/headers/worksheet.tex")

    c = Configuration()
    assert c == {}

    c.header = "INVALID.tex"
    assert c == {}

    c.header = "exam.tex"
    assert c == {"header": exam}

    c.header = "INVALID.tex"
    assert c == {"header": exam}

    c.header = "worksheet"
    assert c == {"header": worksheet}

    c.header = exam
    assert c == {"header": exam}
