import pytest

from draft.models.configuration import Configuration


def test_user_values():
    """
    Testing Configuration().user_values

    Expected behaviour:
    - Traversal to root works | NOT TESTED
    - Files closer to call site take precedence | NOT TESTED
    """
    user_values = Configuration().user_values
    expectation = {
        'author': 'TH',
        'semester': 'SoSe 2023',
        'place': 'Stuttgart',
        'course': 'HE 2',
    }
    assert user_values == expectation
