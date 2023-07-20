from craft_documents.Prompter import List

"""
List.default
├── case int(value)  
│   ├── value in range(0, len(choices))  # 1
│   │   ↪ set default
│   └── value > len(choices)  # 2
│       ↪ don't set default
└── case str(value)
    ├── value in choices  # 3
    │   ↪ set default
    └── value not in choices  # 4
        ↪ don't set default
"""


def test_default_1():
    choices = ["one"]
    e = List(
        "name",
        choices=choices,
        default=0,
    )

    assert e.default == 0


def test_default_2():
    choices = ["one"]
    e = List(
        "name",
        choices=choices,
        default=1,
    )

    assert e.default == None


def test_default_3():
    choices = ["one"]
    e = List(
        "name",
        choices=choices,
        default="one",
    )

    assert e.default == "one"


def test_default_4():
    choices = ["one"]
    e = List(
        "name",
        choices=choices,
        default="two",
    )

    assert e.default == None
