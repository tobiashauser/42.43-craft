from pathlib import Path
from typing import List

import yaml

from draft.configuration.DraftExercisesValidator import DraftExercisesValidator
from tests.configuration.test_Configuration import Configuration


def test_yaml_typing_str():
    input = """
draft-exercises: intervals
"""
    y = yaml.safe_load(input)
    assert y == {"draft-exercises": "intervals"}
    assert isinstance(y["draft-exercises"], str)


def test_yaml_typing_list_str():
    input = """
draft-exercises: 
    - intervals
    - chords
"""
    y = yaml.safe_load(input)
    assert y == {"draft-exercises": ["intervals", "chords"]}
    assert type(y["draft-exercises"]) == list

    match y["draft-exercises"]:
        case list():
            assert True
        case _:
            assert False


def test_yaml_typing_dict_one():
    input = """
draft-exercises:
    intervals:
        count: 2
        path: "intervals.tex"
"""
    y = yaml.safe_load(input)
    assert y == {
        "draft-exercises": {
            "intervals": {
                "count": 2,
                "path": "intervals.tex",
            },
        }
    }
    assert type(y["draft-exercises"]) == dict

    match y["draft-exercises"]:
        case dict(value):
            assert value == {"intervals": {"count": 2, "path": "intervals.tex"}}
        case _:
            assert False


def test_yaml_typing_list_of_dict():
    input = """
draft-exercises:
    - intervals: 1
    - chords: 
        count: 2
    - melody
"""
    y = yaml.safe_load(input)
    assert y == {
        "draft-exercises": [{"intervals": 1}, {"chords": {"count": 2}}, "melody"]
    }

    match y["draft-exercises"]:
        case list(value):
            for element in value:
                match element:
                    case dict():
                        assert True
                    case str():
                        assert True
                    case _:
                        assert False
        case _:
            assert False


def test_yaml_typing_list_with_dict():
    input = """
draft-exercises:
    - intervals:
        count: 3
        path: blob
    - chords: 2
"""
    y = yaml.safe_load(input)
    assert y == {
        "draft-exercises": [
            {"intervals": {"count": 3, "path": "blob"}},
            {"chords": 2},
        ]
    }


def test_yaml_typing_dict():
    input = """
draft-exercises:
    intervals: 1
    chords:
        count: 3
"""
    y = yaml.safe_load(input)
    assert y == {"draft-exercises": {"intervals": 1, "chords": {"count": 3}}}


intervals = Path(
    "/Users/tobiashauser/Binder/40-49 Projects/42 Programmieren/42.43 draft/config.draft/exercises/intervals.tex"
)


def test_linter_str():
    v = DraftExercisesValidator()
    c = Configuration()
    v._configuration = c

    assert {"intervals": {"count": 1, "path": intervals}} == v.lint("intervals.tex")


def test_linter_list_str():
    v = DraftExercisesValidator()
    c = Configuration()
    v._configuration = c

    assert {"intervals": {"count": 1, "path": intervals}} == v.lint(["intervals"])


def test_linter_list_dict_str_int():
    v = DraftExercisesValidator()
    c = Configuration()
    v._configuration = c

    assert {"intervals": {"count": 2, "path": intervals}} == v.lint(
        [{"intervals.tex": 2}]
    )


def test_linter_list_dict_str_dict():
    v = DraftExercisesValidator()
    c = Configuration()
    v._configuration = c

    assert {
        "intervals": {
            "count": 2,
            "path": intervals.parent / "blob.tex",
            "blib": "blob",
        }
    } == v.lint(
        [
            {
                "intervals.tex": {
                    "count": 2,
                    "path": "blob",
                    "blib": "blob",
                }
            }
        ]
    )


def test_linter_dict_int():
    v = DraftExercisesValidator()
    c = Configuration()
    v._configuration = c

    assert {"intervals": {"count": 2, "path": intervals}} == v.lint(
        {"intervals.tex": 2}
    )


def test_linter_dict_dict():
    v = DraftExercisesValidator()
    c = Configuration()
    v._configuration = c

    assert {"intervals": {"count": 3, "path": intervals, "blib": "blob"}} == v.lint(
        {"intervals.tex": {"count": 3, "blib": "blob"}}
    )


def test_run_no_input():
    v = DraftExercisesValidator()
    c = Configuration()
    v.run(c)

    assert c == {}


def test_run_valid_input():
    v = DraftExercisesValidator()
    c = Configuration()
    c[v.key] = {"intervals": 2}
    v.run(c)

    assert c == {"draft-exercises": {"intervals": {"count": 2, "path": intervals}}}


def test_run_multiple_valid_input():
    v = DraftExercisesValidator()
    c = Configuration()
    c[v.key] = {
        "intervals": 2,
        "chords": 1,
    }  # chords is removed because it doesn't exist yet
    v.run(c)

    assert c == {"draft-exercises": {"intervals": {"count": 2, "path": intervals}}}


def test_run_invalid_input():
    v = DraftExercisesValidator()
    c = Configuration()
    c[v.key] = Path()
    v.run(c)

    assert c == {}


def test_run_invalid_path():
    v = DraftExercisesValidator()
    c = Configuration()
    c[v.key] = {"intervals": {"count": 1, "path": Path()}}
    v.run(c)

    assert c == {}


def test_run_invalid_count():
    v = DraftExercisesValidator()
    c = Configuration()
    c[v.key] = {"intervals": {"count": -1, "path": intervals}}
    v.run(c)

    assert c == {}
