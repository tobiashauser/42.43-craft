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
\newcommand{\header}[]{Defined in the header.}

\begin{document}
Hello, <<planet>>!

<<draft-exercises>>
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
\newcommand{\lorem}[]{Defined in the exercise.}

\begin{document}
\exercise{Intervalle}{<<points>>}
This exercise has <<interval-count>> intervals.
\lilypondfile{intervals.ly}
\end{document}
"""


class Preamble(PreambleTest):
    def load(self):
        self._contents = preamble_contents
        self.remove_document_body()


class Header(HeaderTest):
    def load(self):
        self._contents = header_contents
        self.remove_documentclass()
        self.remove_include_preamble()


class Exercise(ExerciseTest):
    def load(self):
        self._contents = exercise_contents
        # TODO: control supplements


class Compiler(LiveCompiler):
    """
    Subclass of compiler whose dependencies are controlled.
    Used when live-testing the tool via `make debug`.
    """

    def __init__(self, configuration: Configuration):
        """
        Add any kwargs that should not be prompted for
        when live testing the debug version.
        """

        # never uncomment...
        configuration["draft-exercises"] = {"intervals": 2}
        configuration.header = "exam.tex"
        configuration["document-name"] = "test"

        # can be customized
        # configuration["remove_comments"] = True
        # configuration["unique_exercise_placeholders"] = False

        # placeholders
        # configuration["planet"] = "Pluto"
        # configuration["semantic-name"] = "Klausur"
        # configuration["semester"] = "SoSe 2023"
        # configuration["place"] = "Stuttgart"
        # configuration["group"] = "Gruppe 1"
        # configuration["course"] = "HE 2"
        # configuration["interval-count"] = "3"
        # configuration["points"] = "2"

        configuration.validate()
        super().__init__(configuration)

    def testing(self):
        """Control included documents for testing."""
        self.configuration["planet"] = "Pluto"
        self.configuration["semantic-name"] = "Klausur"
        self.configuration["semester"] = "SoSe 2023"
        self.configuration["place"] = "Stuttgart"
        self.configuration["group"] = "Gruppe 1"
        self.configuration["course"] = "HE 2"
        self.configuration["interval-count"] = "3"
        self.configuration["points"] = "2"
        self.configuration["document-name"] = "test"
        self.configuration["remove_comments"] = True
        self.configuration["unique_exercise_placeholders"] = False

        self.configuration.validate()

        self._preamble = Preamble(path=Path("preamble.tex"), configuration=self.configuration)  # type: ignore
        self._header = Header(path=Path("header.tex"), configuration=self.configuration)  # type: ignore

        self.configuration["draft-exercises"] = {"exercise": {"count": 2}}
        self._exercises = [  # type: ignore
            Exercise(configuration=self.configuration),  # type: ignore
            Exercise(configuration=self.configuration),  # type: ignore
        ]
        self.disambiguate_exercises()


def test_testCompiler():
    configuration = Configuration(key="value")
    c = Compiler(configuration)
    c.testing()

    assert c.configuration["key"] == "value"
    assert c.exercises[0].disambiguated_name == "exercise-1"


def test_jobs_after_compile():
    c = Compiler(Configuration())
    c.testing()

    assert c.jobs == {}

    try:
        c.compile()
    except:
        raise Exception("Prompting the user is not allowed in tests.")

    assert c.jobs == {
        Path(
            "test.tex"
        ): r"""% Preamble ------------------------------------------------------------------- %

\documentclass{scrreport}

\newcounter{exerciseCounter}
\newcommand{\exercise}[2]{%
  \stepcounter{exerciseCounter}
  \vspace{1em}%
  \noindent%
  \textbf{{\Large Aufgabe\hspace{1mm}\arabic{exerciseCounter}:\hspace{1mm}#1}\hfill{\normalsize/#2}}%
  \vspace{1em}
}

% Header -------------------------------------------------------------------- %

\newcommand{\header}[]{Defined in the header.}

% exercise-1 ----------------------------------------------------------------- %

\newcommand{\lorem}[]{Defined in the exercise.}

% exercise-2 ----------------------------------------------------------------- %

\newcommand{\lorem}[]{Defined in the exercise.}

\begin{document}
Hello, Pluto!

% exercise-1 ----------------------------------------------------------------- %
\exercise{Intervalle}{2}
This exercise has 3 intervals.
\lilypondfile{intervals.ly}
% exercise-2 ----------------------------------------------------------------- %
\exercise{Intervalle}{2}
This exercise has 3 intervals.
\lilypondfile{intervals.ly}

\end{document}
""",
    }
