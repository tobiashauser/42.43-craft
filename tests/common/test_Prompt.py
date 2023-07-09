from draft.common.Prompt import List, PromptType


def test_list():
    # auto-generated message
    p = List(name="test", choices=["one", "two"], default="two")
    assert p == {
        "name": "test",
        "choices": ["one", "two"],
        "default": "two",
        "message": "Please provide a value for 'test'.",
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
        "message": "Please provide a value for 'test'.",
        "type": "list",
    }

    # default index out of bounds
    p = List(name="test", choices=["one", "two"], default=2)
    assert p == {
        "name": "test",
        "choices": ["one", "two"],
        "message": "Please provide a value for 'test'.",
        "type": "list",
    }

    # default as callable and all other callables
    callable = lambda answers: "hello"
    when = lambda answers: True
    filter = lambda value: "hello"
    p = List(
        name="test", choices=["one", "two"], default=callable, when=when, filter=filter
    )
    assert p == {
        "name": "test",
        "choices": ["one", "two"],
        "default": callable,
        "message": "Please provide a value for 'test'.",
        "type": "list",
        "when": when,
        "filter": filter,
    }
