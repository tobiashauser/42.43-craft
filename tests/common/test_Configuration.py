from pathlib import Path
from typing import Dict

from draft.common.Configuration import Configuration as LiveConfiguration


class Configuration(LiveConfiguration):
    def load(self):
        pass


def test_live_loading():
    root = Path("draftrc")
    cwd = Path("tests/draftrc")

    with root.open("w") as file:
        file.write("A: 1\nB: 2")

    with cwd.open("w") as file:  # takes precedence
        file.write("A: 3\nC: 4")

    c = LiveConfiguration(root=Path(), cwd=Path("tests"))
    expectation: Dict[str, int] = {"A": 3, "B": 2, "C": 4}

    assert c == expectation

    root.unlink()
    cwd.unlink()


def test_instantiation():
    c = Configuration(A=1, B=2)
    assert c["A"] == 1
    assert c["B"] == 2
