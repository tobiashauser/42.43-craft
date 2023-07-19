from typing import Any, Dict

from craft_documents.common.helpers import *


def test_combine_dictionaries():
    one: Dict[Any, Any] = {
        "A": "one",
        "B": [1, 2, 3],
        "C": {"a": [1]},
        "D": [1, 2],
    }
    two: Dict[Any, Any] = {
        "A": "two",
        "B": [4],
        "C": {"a": [2]},
        "D": 3,
    }
    expectation: Dict[Any, Any] = {
        "A": "one",  # two didn't overwrite this value
        "B": [1, 2, 3, 4],  # [1, 2, 3] + [4]
        "C": {"a": [1, 2]},  # combined dictionaries
        "D": [1, 2],  # not both are lists
    }

    assert combine_dictionaries(one, two) == expectation
