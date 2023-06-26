from pathlib import Path

from draft.common.Configuration import Configuration
from draft.common.TexTemplate import TexTemplate


class TexTemplateImplementation(TexTemplate):
    def __init__(
        self, configuration: Configuration = Configuration(), path: Path = Path()
    ):
        super().__init__(configuration=configuration, path=path)

    def load(self):
        self._contents = ""


def test_remove_parts_of_contents():
    t = TexTemplateImplementation()
    input = r"""
\documentclass{scrreport}

\input{preamble}
\input{../../preamble.tex}

\begin{document}
Hello, world!
\end{document}
"""
    input = t.remove_document_body(input)
    assert (
        input
        == "\\documentclass{scrreport}\n\n\\input{preamble}\n\\input{../../preamble.tex}"
    )

    input = t.remove_include_preamble(input)
    assert input == "\\documentclass{scrreport}"
