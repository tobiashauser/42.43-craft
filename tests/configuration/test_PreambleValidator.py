from pathlib import Path

from craft_documents.configuration.PreambleValidator import PreambleValidator
from tests.configuration.test_Configuration import Configuration


def test_Lint_Relative_Path(request):
    default = Path(request.config.rootdir / "config.craft/preambles/default.tex")
    c = Configuration()
    v = PreambleValidator()
    v._configuration = c

    assert default == v.lint("default")
    assert default == v.lint("default.tex")


def test_Lint_Absolute_Path(request):
    default = Path(request.config.rootdir / "config.craft/preambles/default.tex")
    c = Configuration()
    v = PreambleValidator()
    v._configuration = c

    assert default == v.lint(default.__str__())


def test_validate_Success(request):
    default = Path(request.config.rootdir / "config.craft/preambles/default.tex")
    v = PreambleValidator()
    assert v.validate(default.__str__())


def test_validate_Failing(request):
    default = Path(request.config.rootdir / "config.craft/preambles/default.tex")
    v = PreambleValidator()
    assert not v.validate(default.parent.__str__() + "INVALID.tex")


def test_resolve(request):
    default = Path(request.config.rootdir / "config.craft/preambles/default.tex")
    c = Configuration()
    v = PreambleValidator()
    v._configuration = c

    assert default == v.default()


def test_run_missing_key(request):
    default = Path(request.config.rootdir / "config.craft/preambles/default.tex")
    c = Configuration()
    v = PreambleValidator()
    v.run(c)

    assert c == {"preamble": default}


def test_run_relative_key(request):
    default = Path(request.config.rootdir / "config.craft/preambles/default.tex")
    c = Configuration(preamble="default.tex")
    v = PreambleValidator()
    v.run(c)
    assert c == {"preamble": default}

    c = Configuration(preamble="default")
    v = PreambleValidator()
    v.run(c)
    assert c == {"preamble": default}


def test_run_invalid_key(request):
    default = Path(request.config.rootdir / "config.craft/preambles/default.tex")
    c = Configuration(preamble="INVALID.tex")
    v = PreambleValidator()
    v.run(c)

    assert c == {"preamble": default}
