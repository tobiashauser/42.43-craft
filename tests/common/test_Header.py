from pathlib import Path

from draft.common.Header import Header as LiveHeader

contents = r"""
\documentclass{scrreport}
"""


class Header(LiveHeader):
    def load(self):
        self._contents = contents


def test_live_loading():
    path = Path("tests/common/test_live_loading.tex")
    contents = r"""
\documentclass{scrreport}
\input{../preamble.tex}

\begin{document}
Hello, world!
\end{document}
"""
    with path.open("w") as file:
        file.write(contents)
    input = LiveHeader(path=path)
    assert input.contents == "\\documentclass{scrreport}"
    path.unlink()


def test_inherited_properties():
    input = Header(path=Path())
    assert input.path == Path()
    assert input.contents == contents
    assert input.placeholders == set()
    assert input.prompts == []
    assert input.yaml == {}
