from pathlib import Path

from draft.configuration.HeaderValidator import HeaderValidator
from tests.configuration.test_Configuration import Configuration

default = Path(
    "/Users/tobiashauser/Binder/40-49 Projects/42 Programmieren/42.43 draft/config.draft/headers/exam.tex"
)


def test_Lint_Relative_Path():
    c = Configuration()
    v = HeaderValidator()
    v._configuration = c

    assert default == v.lint("exam")
    assert default == v.lint("exam.tex")


def test_Lint_Absolute_Path():
    c = Configuration()
    v = HeaderValidator()
    v._configuration = c

    assert default == v.lint(default.__str__())


def test_validate_Success():
    v = HeaderValidator()
    assert v.validate(default.__str__())


def test_validate_Failing():
    v = HeaderValidator()
    c = Configuration()
    v._configuration = c
    assert not v.validate(default.parent.__str__() + "INVALID.tex")


def test_run_missing_key():
    c = Configuration()
    v = HeaderValidator()
    v.run(c)

    assert c == {}


def test_run_relative_key():
    c = Configuration(header="exam.tex")
    v = HeaderValidator()
    v.run(c)
    assert c == {"header": default}

    c = Configuration(header="exam")
    v = HeaderValidator()
    v.run(c)
    assert c == {"header": default}


def test_run_invalid_key():
    c = Configuration(header="INVALID.tex")
    v = HeaderValidator()
    v.run(c)

    assert c == {}
