from pathlib import Path

from draft.common.Configuration import Configuration
from draft.common.Header import Header as LiveHeader
from tests.common.test_Configuration import Configuration

contents = r"""
\documentclass{scrreport}

\begin{document}
Hello, world!
\end{document}
"""


class Header(LiveHeader):
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
    _contents = r"""
\documentclass{scrreport}
\input{../preamble.tex}

\begin{document}
Hello, world!
\end{document}
"""
    with path.open("w") as file:
        file.write(_contents)
    input = LiveHeader(path=path, configuration=Configuration())
    assert input.contents == contents
    path.unlink()


def test_inherited_properties():
    input = Header()
    assert input.path == Path("jane.tex")
    assert input.contents == contents
    assert input.placeholders == set()
    assert input.prompts == []
    assert input.yaml == {}
