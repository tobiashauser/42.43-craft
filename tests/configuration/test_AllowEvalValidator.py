from draft.configuration.AllowEvalValidator import MultipleExercisesValidator
from tests.configuration.test_Configuration import Configuration


def test_validate_Success():
    v = MultipleExercisesValidator()
    assert v.validate(False)
    assert v.validate(True)


def test_validate_Failing():
    v = MultipleExercisesValidator()
    assert not v.validate("not a bool")  # type: ignore


def test_resolve():
    c = Configuration()
    v = MultipleExercisesValidator()
    v._configuration = c

    assert False == v.default()


def test_run_missing_key():
    c = Configuration()
    v = MultipleExercisesValidator()
    v.run(c)

    assert c == {"allow_eval": False}


def test_run_key_true():
    c = Configuration(allow_eval=True)
    assert c == {"allow_eval": True}
    v = MultipleExercisesValidator()
    v.run(c)
    assert c == {"allow_eval": True}


def test_run_key_false():
    c = Configuration(allow_eval=False)
    v = MultipleExercisesValidator()
    v.run(c)
    assert c == {"allow_eval": False}


def test_run_invalid_key():
    c = Configuration(allow_eval="not a bool")
    v = MultipleExercisesValidator()
    v.run(c)

    assert c == {"allow_eval": False}
