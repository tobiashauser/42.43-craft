from pathlib import Path
from typing import Any, Dict

import oyaml as yaml

from draft.common.Configuration import Configuration as LiveConfiguration
from draft.common.helpers import combine_dictionaries


class Configuration(LiveConfiguration):
    """
    This class can be used for testing. It
    doesn't reach into the environment at all;
    only inside this repository.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            Path("configuration/draftrc"), Path(), Path("tests"), *args, **kwargs
        )


def test_live_loading():
    configuration = yaml.safe_load(Path("configuration/draftrc").open())
    root = Path("draftrc")
    cwd = Path("tests/draftrc")

    with root.open("w") as file:
        file.write("A: 1\nB: 2")

    with cwd.open("w") as file:  # takes precedence
        file.write("A: 3\nC: 4")

    c = LiveConfiguration(
        main=Path("configuration/draftrc"), root=Path(), cwd=Path("tests")
    )
    expectation: Dict[str, Any] = combine_dictionaries(
        configuration, {"A": 3, "B": 2, "C": 4}
    )

    assert c == expectation

    root.unlink()
    cwd.unlink()


def test_instantiation():
    c = Configuration(A=1, B=2)
    assert c["A"] == 1
    assert c["B"] == 2


def test_reference_semantics():
    c = Configuration(A=1, B=2)
    assert len(c) == 3

    copy = c
    copy["A"] = 3

    assert c["A"] == 3

    copy["C"] = 4

    assert len(c) == 4
    assert c["C"] == 4
