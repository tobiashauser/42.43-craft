from pathlib import Path

from draft.common.Configuration import Configuration
from draft.common.Header import Header as LiveHeader

contents = r"""
\documentclass{scrreport}

\begin{document}
Hello, world!
\end{document}
"""


class Header(LiveHeader):
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
    input = LiveHeader(configuration=Configuration(), path=path)
    assert input.contents == contents.strip()
    path.unlink()


def test_inherited_properties():
    input = Header(configuration=Configuration(), path=Path())
    assert input.path == Path()
    assert input.contents == contents
    assert input.placeholders == set()
    assert input.prompts == []
    assert input.yaml == {}
