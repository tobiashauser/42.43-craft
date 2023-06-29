from pathlib import Path

from draft.common.Configuration import Configuration
from draft.common.TexTemplate import TexTemplate


class TexTemplateImplementation(TexTemplate):
    def __init__(self, contents: str):
        self._contents = contents
        super().__init__(configuration=Configuration(), path=Path())

    def load(self):
        pass


def test_remove_document_body():
    input = r"""
\documentclass{scrreport}

\input{preamble}
\input{../../preamble.tex}

\begin{document}
Hello, world!
\end{document}
"""

    t = TexTemplateImplementation(input)
    t.remove_document_body()

    assert (
        t.contents
        == r"""
\documentclass{scrreport}

\input{preamble}
\input{../../preamble.tex}

"""
    )


def test_remove_include_preamble():
    input = r"""
\documentclass{scrreport}

\input{preamble}
\input{../../preamble.tex}

\begin{document}
Hello, world!
\end{document}
"""

    t = TexTemplateImplementation(input)
    t.remove_include_preamble()

    assert (
        t.contents
        == r"""
\documentclass{scrreport}

\begin{document}
Hello, world!
\end{document}
"""
    )
