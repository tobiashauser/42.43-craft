from pathlib import Path

from draft.configuration.Configuration import Configuration
from draft.configuration.DraftExercisesValidator import ExerciseConfiguration
from draft.new.Compiler import Compiler as LiveCompiler
from tests.common.test_common_Configuration import Configuration
from tests.common.test_Exercise import ExerciseTest
from tests.common.test_Header import Header as HeaderTest
from tests.common.test_Preamble import Preamble as PreambleTest

preamble_contents = r"""
% TESTING %
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
% TESTING %
\documentclass{scrreport}

\input{../preambles/default}

\begin{document}
Hello, world!
\end{document}
"""

exercise_contents = r"""
% TESTING %
\iffalse
# supplements:
#  - intervals.ly
unique-placeholders:
  - interval-count
\fi

\input{../preambles/default.tex}

\begin{document}
\exercise{Intervalle}{<<points>>}
This exercise has <<interval-count>> intervals.
\lilypondfile{<<supplements/intervals.ly>>}
\end{document}
"""


class Preamble(PreambleTest):
    def load(self):
        self._contents = preamble_contents


class Header(HeaderTest):
    def load(self):
        self._contents = header_contents


class Exercise(ExerciseTest):
    def load(self):
        self._contents = exercise_contents
        # TODO: control supplements


class Compiler(LiveCompiler):
    def __init__(self, configuration: Configuration):
        # Add any kwargs that should not be prompted for when
        # live testing the debug version
        configuration.header = "exam.tex"
        configuration["draft-exercises"] = {"intervals": 2}

        configuration.validate()
        super().__init__(configuration)

    def testing(self):
        """Control included documents for testing."""
        self._preamble = Preamble(configuration=self.configuration)  # type: ignore
        self._header = Header(configuration=self.configuration)  # type: ignore
        self._exercises = [  # type: ignore
            Exercise(configuration=self.configuration),  # type: ignore
            Exercise(configuration=self.configuration),  # type: ignore
        ]


def test_testCompiler():
    configuration = Configuration(key="value")
    c = Compiler(configuration)
    c.testing()

    assert c.configuration["key"] == "value"
    assert c.preamble.contents == preamble_contents
    assert c.header.contents == header_contents
    assert len(c.exercises) == 2
    assert c.exercises[0].contents == exercise_contents
