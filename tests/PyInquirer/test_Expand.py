from craft_documents.Prompter import Expand

"""
Expand.default
├── case int(value)  
│   ├── value in range(0, len(choices))  # 1
│   │   ↪ set default
│   └── value > len(choices)  # 2
│       ↪ don't set default
└── case str(value)
    ├── value in choices.keys  # 3
    │   ↪ set default
    └── value not in choices.keys  # 4
        ↪ don't set default
"""


def test_default_1():
    choices = [Expand.Choice(name="one", key="a")]
    e = Expand(
        "name",
        choices=choices,
        default=0,
    )

    assert e.default == 0


def test_default_2():
    choices = [Expand.Choice(name="one", key="a")]
    e = Expand(
        "name",
        choices=choices,
        default=1,
    )

    assert e.default == None


def test_default_3():
    choices = [Expand.Choice(name="one", key="a")]
    e = Expand(
        "name",
        choices=choices,
        default="a",
    )

    assert e.default == "a"


def test_default_4():
    choices = [Expand.Choice(name="one", key="a")]
    e = Expand(
        "name",
        choices=choices,
        default="b",
    )

    assert e.default == None
