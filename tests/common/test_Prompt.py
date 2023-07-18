import collections.abc

from craft_documents.common.Prompt import Expand, List

collections.Mapping = collections.abc.Mapping  # type: ignore
from PyInquirer import Separator


def test_list():
    # auto-generated message
    p = List(name="test", choices=["one", "two"], default="two")
    assert p == {
        "name": "test",
        "choices": ["one", "two"],
        "default": "two",
        "message": "Please provide the 'test'.",
        "type": "list",
    }

    # custom message
    p = List(name="test", choices=["one", "two"], default=1, message="Choose!!")
    assert p == {
        "name": "test",
        "choices": ["one", "two"],
        "default": 1,
        "message": "Choose!!",
        "type": "list",
    }

    # default not in choices
    p = List(name="test", choices=["one", "two"], default="three")
    assert p == {
        "name": "test",
        "choices": ["one", "two"],
        "message": "Please provide the 'test'.",
        "type": "list",
    }

    # default index out of bounds
    p = List(name="test", choices=["one", "two"], default=2)
    assert p == {
        "name": "test",
        "choices": ["one", "two"],
        "message": "Please provide the 'test'.",
        "type": "list",
    }

    # default as callable and all other callables
    callable = lambda answers: "hello"
    when = lambda answers: True
    filter = lambda value: "hello"
    p = List(
        name="test",
        choices=["one", "two"],
        default=callable,
        when=when,
        filter=filter,
    )
    assert p == {
        "name": "test",
        "choices": ["one", "two"],
        "default": callable,
        "message": "Please provide the 'test'.",
        "type": "list",
        "when": when,
        "filter": filter,
    }


def test_Expand():
    c1 = Expand.Choice("blob", "b", "blob")
    s = Separator()
    e = Expand(name="test", choices=[c1, s], default="b")
    assert e == {
        "name": "test",
        "message": "Please provide the 'test'.",
        "type": "expand",
        "choices": [c1, s],
        "default": "b",
    }

    # default is invalid
    e = Expand(name="test", choices=[c1, s], default="x")
    assert e == {
        "name": "test",
        "message": "Please provide the 'test'.",
        "type": "expand",
        "choices": [c1, s],
    }

    # is dict["key"] = None entered? Yes, it is
    c1 = Expand.Choice(name="blob", key="b")  # value is None
    assert c1 == {"key": "b", "name": "blob"}
