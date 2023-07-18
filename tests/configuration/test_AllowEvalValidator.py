from craft_documents.configuration.AllowEvalValidator import AllowEvalValidator
from tests.configuration.test_Configuration import Configuration


def test_validate_Success():
    v = AllowEvalValidator()
    assert v.validate(False)
    assert v.validate(True)


def test_validate_Failing():
    v = AllowEvalValidator()
    assert not v.validate("not a bool")  # type: ignore


def test_resolve():
    c = Configuration()
    v = AllowEvalValidator()
    v._configuration = c

    assert False == v.default()


def test_run_missing_key():
    c = Configuration()
    v = AllowEvalValidator()
    v.run(c)

    assert c == {"allow_eval": False}


def test_run_key_true():
    c = Configuration(allow_eval=True)
    assert c == {"allow_eval": True}
    v = AllowEvalValidator()
    v.run(c)
    assert c == {"allow_eval": True}


def test_run_key_false():
    c = Configuration(allow_eval=False)
    v = AllowEvalValidator()
    v.run(c)
    assert c == {"allow_eval": False}


def test_run_invalid_key():
    c = Configuration(allow_eval="not a bool")
    v = AllowEvalValidator()
    v.run(c)

    assert c == {"allow_eval": False}
