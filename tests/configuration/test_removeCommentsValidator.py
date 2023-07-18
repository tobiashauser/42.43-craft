from pathlib import Path

from craft_documents.configuration.RemoveCommentsValidator import (
    RemoveCommentsValidator,
)
from tests.configuration.test_Configuration import Configuration


def test_validate_Success():
    v = RemoveCommentsValidator()
    assert v.validate(False)
    assert v.validate(True)


def test_validate_Failing():
    v = RemoveCommentsValidator()
    assert not v.validate("not a bool")  # type: ignore


def test_resolve():
    c = Configuration()
    v = RemoveCommentsValidator()
    v._configuration = c

    assert False == v.default()


def test_run_missing_key():
    c = Configuration()
    v = RemoveCommentsValidator()
    v.run(c)

    assert c == {"remove_comments": False}


def test_run_key_true():
    c = Configuration(remove_comments=True)
    assert c == {"remove_comments": True}
    v = RemoveCommentsValidator()
    v.run(c)
    assert c == {"remove_comments": True}


def test_run_key_false():
    c = Configuration(remove_comments=False)
    v = RemoveCommentsValidator()
    v.run(c)
    assert c == {"remove_comments": False}


def test_run_invalid_key():
    c = Configuration(remove_comments="not a bool")
    v = RemoveCommentsValidator()
    v.run(c)

    assert c == {"remove_comments": False}
