from pathlib import Path

from draft.common.Preamble import Preamble as LivePreamble

contents = r"""
\documentclass{scrreport}
"""


class Preamble(LivePreamble):
    def load(self):
        self._contents = contents


def test_live_loading():
    path = Path("tests/common/test_live_loading.tex")
    contents = r"""
\documentclass{scrreport}

\begin{document}
Hello, world!
\end{document}
"""
    with path.open("w") as file:
        file.write(contents)
    input = LivePreamble(path=path)
    assert input.contents == "\\documentclass{scrreport}"
    path.unlink()


def test_inherited_properties():
    input = Preamble(path=Path())
    assert input.path == Path()
    assert input.contents == contents
    assert input.placeholders == set()
    assert input.prompts == []
    assert input.yaml == {}
