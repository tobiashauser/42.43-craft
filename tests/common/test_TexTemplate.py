from pathlib import Path

from draft.common.TexTemplate import TexTemplate
from tests.configuration.test_Configuration import Configuration

contents = r"""
\documentclass{scrreport}

\newcommand{title}{}

\begin{document}
Hello, world!
\end{document}
"""


class TexTemplateImplementation(TexTemplate):
    def __init__(self, contents: str):
        self._contents = contents
        super().__init__(
            configuration=Configuration(),
            path=Path("jane.tex"),
        )

    def load(self):
        pass


def test_return_document_body():
    t = TexTemplateImplementation(contents)
    assert t.body == "Hello, world!\n"


def test_return_declarations():
    t = TexTemplateImplementation(contents)
    assert (
        t.declarations
        == r"""
\documentclass{scrreport}

\newcommand{title}{}

"""
    )
    assert t.contents == contents


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

\input{../preambles/preamble}
\input{../preambles/default.tex}

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
