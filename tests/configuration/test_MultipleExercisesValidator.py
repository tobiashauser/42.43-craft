from pathlib import Path

from draft.configuration.MultipleExercisesValidator import MultipleExercisesValidator
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

    assert True == v.default()


def test_run_missing_key():
    c = Configuration()
    v = MultipleExercisesValidator()
    v.run(c)

    assert c == {"multiple-exercises": True}


def test_run_key_true():
    c = Configuration()
    c["multiple-exercises"] = True
    assert c == {"multiple-exercises": True}
    v = MultipleExercisesValidator()
    v.run(c)
    assert c == {"multiple-exercises": True}


def test_run_key_false():
    c = Configuration()
    c["multiple-exercises"] = False
    v = MultipleExercisesValidator()
    v.run(c)
    assert c == {"multiple-exercises": False}


def test_run_invalid_key():
    c = Configuration()
    c["multiple-exercises"] = "not a bool"
    v = MultipleExercisesValidator()
    v.run(c)

    assert c == {"multiple-exercises": True}
