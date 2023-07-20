import random

from craft_documents.Prompter import Input, Prompter
from craft_documents.Prompter.Prompt import Answers


# initializing with the default values
def test_init_defaults():
    p = Prompter()

    assert p.mode == Prompter.Mode.ALWAYS
    assert p.storage == None


"""
Prompter.ask
├── prompt.name is in storage
│   ├── Mode.STRICT  # 1
│   │   ↪ don't overwrite storage
│   └── Mode.ALWAYS  # 2
│       ↪ overwrite storage
├── prompt.name is not in storage
│   └── Mode.STRICT || Mode.ALWAYS # 3
│       ↪ set storage
├── storage is empty (bug fix)
│   └── Mode.STRICT || Mode.ALWAYS # 4
│       ↪ set storage
└── storage is None
    └── Mode.STRICT || Mode.ALWAYS # 5
        ↪ storage stays None but returns answer
"""


def test_ask_1():
    storage = {"key": "value"}
    p = Prompter(mode=Prompter.Mode.STRICT, storage=storage)

    answer = p.ask(Input("key"))

    assert answer == "value"
    assert p.storage is storage
    assert storage == {"key": "value"}


def test_ask_2():
    storage = {"key": "value"}
    p = Prompter(mode=Prompter.Mode.ALWAYS, storage=storage)

    answer = p.ask(Input("key"))

    assert answer == "INPUT"
    assert p.storage is storage
    assert storage == {"key": "INPUT"}


def test_ask_3():
    mode = random.choice(list(Prompter.Mode))
    storage = {"key": "value"}
    p = Prompter(mode=mode, storage=storage)

    answer = p.ask(Input("newKey"))

    assert answer == "INPUT"
    assert p.storage is storage
    assert storage == {"key": "value", "newKey": "INPUT"}


def test_ask_4():
    mode = random.choice(list(Prompter.Mode))
    storage = {}
    p = Prompter(mode=mode, storage=storage)

    answer = p.ask(Input("key"))

    assert answer == "INPUT"
    assert p.storage is storage
    assert storage == {"key": "INPUT"}


def test_ask_5():
    mode = random.choice(list(Prompter.Mode))
    storage = None
    p = Prompter(mode=mode, storage=storage)

    answer = p.ask(Input("key"))

    assert answer == "INPUT"
    assert p.storage is storage
    assert storage == None
