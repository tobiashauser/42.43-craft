from pathlib import Path

from craft_documents.configuration.PreambleValidator import PreambleValidator
from tests.configuration.test_Configuration import Configuration

default = Path(
    "/Users/tobiashauser/Binder/40-49 Projects/42 Programmieren/42.43 craft/config.craft/preambles/default.tex"
)


def test_Lint_Relative_Path():
    c = Configuration()
    v = PreambleValidator()
    v._configuration = c

    assert default == v.lint("default")
    assert default == v.lint("default.tex")


def test_Lint_Absolute_Path():
    c = Configuration()
    v = PreambleValidator()
    v._configuration = c

    assert default == v.lint(default.__str__())


def test_validate_Success():
    v = PreambleValidator()
    assert v.validate(default.__str__())


def test_validate_Failing():
    v = PreambleValidator()
    assert not v.validate(default.parent.__str__() + "INVALID.tex")


def test_resolve():
    c = Configuration()
    v = PreambleValidator()
    v._configuration = c

    assert default == v.default()


def test_run_missing_key():
    c = Configuration()
    v = PreambleValidator()
    v.run(c)

    assert c == {"preamble": default}


def test_run_relative_key():
    c = Configuration(preamble="default.tex")
    v = PreambleValidator()
    v.run(c)
    assert c == {"preamble": default}

    c = Configuration(preamble="default")
    v = PreambleValidator()
    v.run(c)
    assert c == {"preamble": default}


def test_run_invalid_key():
    c = Configuration(preamble="INVALID.tex")
    v = PreambleValidator()
    v.run(c)

    assert c == {"preamble": default}
