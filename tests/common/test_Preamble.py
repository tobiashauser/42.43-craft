from pathlib import Path

from draft.common.Preamble import Preamble as LivePreamble
from tests.common.test_common_Configuration import Configuration

contents = r"""
\documentclass{scrreport}

<<one>>

"""
# the document body is beeing stripped -> test_live_loading


class Preamble(LivePreamble):
    def __init__(
        self,
        path: Path = Path("jane.tex"),
        configuration: Configuration = Configuration(),
    ):
        super().__init__(path, configuration)

    def load(self):
        self._contents = contents


def test_live_loading():
    path = Path("tests/common/test_live_loading.tex")
    contents = r"""
\documentclass{scrreport}

<<one>>
"""
    with path.open("w") as file:
        file.write(contents)

    input = LivePreamble(path=path, configuration=Configuration())
    assert (
        input.contents
        == r"""
\documentclass{scrreport}

<<one>>
"""
    )
    assert input.placeholders == {"one"}  # <<world>> is removed

    path.unlink()


def test_inherited_properties():
    input = Preamble()
    assert input.path == Path("jane.tex")
    assert input.contents == contents
    assert input.placeholders == {"one"}
    assert len(input.prompts) == 1
    assert input.prompts[0]["name"] == "one"
    assert input.yaml == {}
