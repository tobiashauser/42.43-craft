from pathlib import Path

from draft.new.Compiler import Compiler
from tests.common.test_Header import Header as HeaderTest
from tests.common.test_Preamble import Preamble as PreambleTest
from tests.configuration.test_Configuration import Configuration

preamble_contents = r"""
\documentclass{scrreport}

\newcounter{exerciseCounter}
\newcommand{\exercise}[2]{%
  \stepcounter{exerciseCounter}
  \vspace{1em}%
  \noindent%
  \textbf{{\Large Aufgabe\hspace{1mm}\arabic{exerciseCounter}:\hspace{1mm}#1}\hfill{\normalsize/#2}}%
  \vspace{1em}
}

\begin{document}
Hello, world!
\end{document}
"""

header_contents = r"""
\documentclass{scrreport}

\input{../preambles/default}

\begin{document}
Hello, world!
\end{document}
"""


class Preamble(PreambleTest):
    def load(self):
        self._contents = preamble_contents


class Header(HeaderTest):
    def load(self):
        self._contents = header_contents


def test_instantiation():
    configuration = Configuration()
    c = Compiler(
        configuration, Header(path=Path("exam.tex"), configuration=configuration)
    )
    c._preamble = Preamble(path=Path("default.tex"), configuration=configuration)

    assert c.preamble.name == "default"
    assert c.preamble.contents == preamble_contents
    assert c.preamble.configuration is configuration

    assert c.header.name == "exam"
    assert c.header.contents == header_contents
    assert c.header.configuration is configuration
