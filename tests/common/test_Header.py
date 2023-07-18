from pathlib import Path

from craft_documents.common.Header import Header as LiveHeader
from tests.common.test_common_Configuration import Configuration

contents = r"""
\documentclass{scrreport}

\begin{document}
\textbf{Hello, world!}

<<draft-exercises>>
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
\input{../preambles/preamble.tex}

\begin{document}
\textbf{Hello, world!}

<<draft-exercises>>
\end{document}
"""
    with path.open("w") as file:
        file.write(_contents)
    input = LiveHeader(path=path, configuration=Configuration())
    assert (
        input.contents
        == r"""
\begin{document}
\textbf{Hello, world!}

<<draft-exercises>>
\end{document}
"""
    )
    path.unlink()


def test_inherited_properties():
    input = Header()
    # assert input.path == Path("jane.tex")
    assert (
        input.contents
        == r"""
\begin{document}
\textbf{Hello, world!}

<<draft-exercises>>
\end{document}
"""
    )
    assert input.placeholders == {"draft-exercises"}
    assert input.prompts == []
    assert input.yaml == {}


def test_set_draft_exercises_unescaped():
    h = Header()

    assert (
        h.body
        == """\\textbf{Hello, world!}

<<draft-exercises>>
"""
    )

    h.set_draft_exercises(r"\lilypondfile{intervals.ly}")

    assert (
        h.body
        == r"""\textbf{Hello, world!}

\lilypondfile{intervals.ly}
"""
    )
