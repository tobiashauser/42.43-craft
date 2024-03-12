from pathlib import Path

from craft_documents.configuration.HeaderValidator import HeaderValidator
from tests.configuration.test_Configuration import Configuration

def test_setup(request):
    default = Path(request.config.rootdir / "config.craft/headers/exam.tex")


def test_Lint_Relative_Path(request):
    c = Configuration()
    v = HeaderValidator()
    v._configuration = c

    default = Path(request.config.rootdir / "config.craft/headers/exam.tex")

    assert default == v.lint("exam")
    assert default == v.lint("exam.tex")


def test_Lint_Absolute_Path(request):
    c = Configuration()
    v = HeaderValidator()
    v._configuration = c

    default = Path(request.config.rootdir / "config.craft/headers/exam.tex")

    assert default == v.lint(default.__str__())


def test_validate_Success(request):
    v = HeaderValidator()

    default = Path(request.config.rootdir / "config.craft/headers/exam.tex")

    assert v.validate(default.__str__())


def test_validate_Failing(request):
    v = HeaderValidator()
    c = Configuration()
    v._configuration = c

    default = Path(request.config.rootdir / "config.craft/headers/exam.tex")

    assert not v.validate(default.parent.__str__() + "INVALID.tex")


def test_run_missing_key():
    c = Configuration()
    v = HeaderValidator()
    v.run(c)

    assert c == {}


def test_run_relative_key(request):
    default = Path(request.config.rootdir / "config.craft/headers/exam.tex")
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
