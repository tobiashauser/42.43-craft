from pathlib import Path

from draft.configuration.Configuration import Configuration
from draft.new.Compiler import Compiler as LiveCompiler
from tests.common.test_common_Configuration import Configuration
from tests.common.test_Header import Header as HeaderTest
from tests.common.test_Preamble import Preamble as PreambleTest

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


class Compiler(LiveCompiler):
    def __init__(self, configuration: Configuration):
        configuration.header = "exam.tex"  # will be discarded
        super().__init__(configuration)

        # Overwrite with test instances
        self._preamble = Preamble()
        self._header = Header()


class Preamble(PreambleTest):
    def load(self):
        self._contents = preamble_contents


class Header(HeaderTest):
    def load(self):
        self._contents = header_contents


def test_testCompiler():
    c = Compiler(Configuration(key="value"))

    assert c.configuration["key"] == "value"
    assert c.preamble.contents == preamble_contents
    assert c.header.contents == header_contents
