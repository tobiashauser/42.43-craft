from pathlib import Path

from craft_documents.common.File import File


class FileImplementation(File):
    def __init__(self, contents: str):
        super().__init__(path=Path())
        self._contents = contents

    def load(self):
        pass


def test_keep_trailing_comment():
    input = r"Hello % comment"

    f = FileImplementation(input)
    f.remove_lines(prefix="%")
    assert f.contents == input


def test_no_new_lines():
    input = r"% A comment"
    expectation = ""

    f = FileImplementation(input)
    f.remove_lines(prefix="%")
    assert f.contents == expectation


def test_trailing_new_line():
    input = r"""% A comment
"""
    expectation = ""

    f = FileImplementation(input)
    f.remove_lines(prefix="%")
    assert f.contents == expectation


def test_leading_new_line():
    input = r"""
% A comment"""
    expectation = "\n"

    f = FileImplementation(input)
    f.remove_lines(prefix="%")
    assert f.contents == expectation


def test_leading_and_trailing_new_line():
    input = r"""
% A comment
"""
    expectation = "\n"

    f = FileImplementation(input)
    f.remove_lines(prefix="%")
    assert f.contents == expectation


def test_mulitple_lines():
    input = r"""% one
% two"""
    expectation = ""

    f = FileImplementation(input)
    f.remove_lines(prefix=r"\%")
    assert f.contents == expectation


def test_multiple_lines_leading():
    input = r"""
% one
% two"""
    expectation = "\n"

    f = FileImplementation(input)
    f.remove_lines(prefix=r"\%")
    assert f.contents == expectation


def test_multiple_lines_trailing():
    input = r"""% one
% two
"""
    expectation = ""

    f = FileImplementation(input)
    f.remove_lines(prefix=r"\%")
    assert f.contents == expectation


def test_multiple_lines_leading_and_traling():
    input = r"""
% one
% two
"""
    expectation = "\n"

    f = FileImplementation(input)
    f.remove_lines(prefix=r"\%")
    assert f.contents == expectation


def test_single_line_and_contents():
    input = r"""
hello

% one

world
"""
    expectation = r"""
hello

world
"""

    f = FileImplementation(input)
    f.remove_lines(prefix=r"\%")
    assert f.contents == expectation


def test_multiple_lines_and_contents():
    input = r"""
hello

% one
% two

world
"""
    expectation = r"""
hello

world
"""

    f = FileImplementation(input)
    f.remove_lines(prefix=r"\%")
    assert f.contents == expectation


def test_single_line_and_contents_condensed():
    input = r"""
hello-
% one
world
"""
    expectation = r"""
hello-
world
"""

    f = FileImplementation(input)
    f.remove_lines(prefix=r"\%")
    assert f.contents == expectation


def test_multiple_lines_and_contents_condensed():
    input = r"""
hello
% one
% two
-world
"""
    expectation = r"""
hello
-world
"""

    f = FileImplementation(input)
    f.remove_lines(prefix=r"\%")
    assert f.contents == expectation


def test_single_line_and_contents_condensed_leading():
    input = r"""
hello
% one

world
"""
    expectation = r"""
hello

world
"""

    f = FileImplementation(input)
    f.remove_lines(prefix=r"\%")
    assert f.contents == expectation


def test_multiple_lines_and_contents_condensed_leading():
    input = r"""
hello
% one
% two



world
"""
    expectation = r"""
hello

world
"""

    f = FileImplementation(input)
    f.remove_lines(prefix=r"\%")
    assert f.contents == expectation


def test_single_line_and_contents_condensed_trailing():
    input = r"""
hello



% one
world
"""
    expectation = r"""
hello



world
"""

    f = FileImplementation(input)
    f.remove_lines(prefix=r"\%")
    assert f.contents == expectation


def test_multiple_lines_and_contents_condensed_trailing():
    input = r"""
hello

% one
% two
world
"""
    expectation = r"""
hello

world
"""

    f = FileImplementation(input)
    f.remove_lines(prefix=r"\%")
    assert f.contents == expectation


def test_single_lines_with_extra_space_leading():
    input = r"""
hello



% one

world
"""
    expectation = r"""
hello



world
"""

    f = FileImplementation(input)
    f.remove_lines(prefix=r"\%")
    assert f.contents == expectation


def test_single_lines_with_extra_space_trailing():
    input = r"""
hello

% one



world
"""
    expectation = r"""
hello

world
"""

    f = FileImplementation(input)
    f.remove_lines(prefix=r"\%")
    assert f.contents == expectation
