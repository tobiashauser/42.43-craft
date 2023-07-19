from pathlib import Path

from craft_documents.common.File import File


class FileImplementation(File):
    def __init__(self, contents: str):
        super().__init__(path=Path())
        self._contents = contents

    def load(self):
        pass

    def remove_blocks(self):
        return super().remove_blocks(prefix=r"\\iffalse", suffix=r"\\fi")


def test_keep_trailing_comment():
    input = r"""
Hello \iffalse a comment \fi
"""

    f = FileImplementation(input)
    f.remove_blocks()
    assert f.contents == input


def test_no_new_lines():
    input = r"\iffalse A comment \fi"
    expectation = ""

    f = FileImplementation(input)
    f.remove_blocks()
    assert f.contents == expectation


def test_trailing_new_line():
    input = r"""\iffalse
Hello, world!
\fi
"""
    expectation = ""

    f = FileImplementation(input)
    f.remove_blocks()
    assert f.contents == expectation


def test_leading_new_line():
    input = r"""
\iffalse
Hello, world!
\fi"""
    expectation = "\n"

    f = FileImplementation(input)
    f.remove_blocks()
    assert f.contents == expectation


def test_leading_and_trailing_new_line():
    input = r"""
\iffalse
Hello, world!
\fi
"""
    expectation = "\n"

    f = FileImplementation(input)
    f.remove_blocks()
    assert f.contents == expectation


def test_mulitple_lines():
    input = r"""\iffalse
Hello, world!
\fi
\iffalse
Hello, world!
\fi"""
    expectation = ""

    f = FileImplementation(input)
    f.remove_blocks()
    assert f.contents == expectation


def test_multiple_lines_leading():
    input = r"""
\iffalse
Hello, world!
\fi
\iffalse
Hello, world!
\fi"""
    expectation = "\n"

    f = FileImplementation(input)
    f.remove_blocks()
    assert f.contents == expectation


def test_multiple_lines_trailing():
    input = r"""\iffalse
Hello, world!
\fi
\iffalse
Hello, world!
\fi
"""
    expectation = ""

    f = FileImplementation(input)
    f.remove_blocks()
    assert f.contents == expectation


def test_multiple_lines_leading_and_traling():
    input = r"""
\iffalse
Hello, world!
\fi
\iffalse
Hello, world!
\fi
"""
    expectation = "\n"

    f = FileImplementation(input)
    f.remove_blocks()
    assert f.contents == expectation


def test_single_line_and_contents():
    input = r"""
hello

\iffalse
Hello, world!
\fi

world
"""
    expectation = r"""
hello

world
"""

    f = FileImplementation(input)
    f.remove_blocks()
    assert f.contents == expectation


def test_multiple_lines_and_contents():
    input = r"""
hello

\iffalse
Hello, world!
\fi
\iffalse
Hello, world!
\fi

world
"""
    expectation = r"""
hello

world
"""

    f = FileImplementation(input)
    f.remove_blocks()
    assert f.contents == expectation


def test_single_line_and_contents_condensed():
    input = r"""
hello
\iffalse
Hello, world!
\fi
world
"""
    expectation = r"""
hello
world
"""

    f = FileImplementation(input)
    f.remove_blocks()
    assert f.contents == expectation


def test_multiple_lines_and_contents_condensed():
    input = r"""
hello-
\iffalse
Hello, world!
\fi
\iffalse
Hello, world!
\fi
-world
"""
    expectation = r"""
hello-
-world
"""

    f = FileImplementation(input)
    f.remove_blocks()
    assert f.contents == expectation


def test_single_line_and_contents_condensed_leading():
    input = r"""
hello-
\iffalse
Hello, world!
\fi

world
"""
    expectation = r"""
hello-

world
"""

    f = FileImplementation(input)
    f.remove_blocks()
    assert f.contents == expectation


def test_multiple_lines_and_contents_condensed_leading():
    input = r"""
hello
\iffalse
Hello, world!
\fi
\iffalse
Hello, world!
\fi



-world
"""
    expectation = r"""
hello

-world
"""

    f = FileImplementation(input)
    f.remove_blocks()
    assert f.contents == expectation


def test_single_line_and_contents_condensed_trailing():
    input = r"""
hello



\iffalse
Hello, world!
\fi
-world
"""
    expectation = r"""
hello



-world
"""

    f = FileImplementation(input)
    f.remove_blocks()
    assert f.contents == expectation


def test_multiple_lines_and_contents_condensed_trailing():
    input = r"""
hello

\iffalse
Hello, world!
\fi
\iffalse
Hello, world!
\fi
world
"""
    expectation = r"""
hello

world
"""

    f = FileImplementation(input)
    f.remove_blocks()
    assert f.contents == expectation


def test_single_lines_with_extra_space_leading():
    input = r"""
hello



\iffalse
Hello, world!
\fi

world
"""
    expectation = r"""
hello



world
"""

    f = FileImplementation(input)
    f.remove_blocks()
    assert f.contents == expectation


def test_single_lines_with_extra_space_trailing():
    input = r"""
hello

\iffalse
Hello, world!
\fi



world
"""
    expectation = r"""
hello

world
"""

    f = FileImplementation(input)
    f.remove_blocks()
    assert f.contents == expectation
