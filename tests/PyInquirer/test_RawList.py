from craft_documents.Prompter import RawList

"""
List.default
├── case int(value)  
│   ├── value in range(0, len(choices))  # 1
│   │   ↪ set default
│   └── value > len(choices)  # 2
│       ↪ don't set default
"""


def test_default_1():
    choices = ["one"]
    e = RawList(
        "name",
        choices=choices,
        default=0,
    )

    assert e.default == 0


def test_default_2():
    choices = ["one"]
    e = RawList(
        "name",
        choices=choices,
        default=1,
    )

    assert e.default == None
