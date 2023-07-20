from craft_documents.Prompter.Prompt import Prompt


class PromptSubclass(Prompt):
    pass


"""
Prompt.message
├── default  # 1
└── custom 
    ├── message="CUSTOMIZED"  # 2
    │   ↪ should override default
    └── message=""  # 3
        ↪ fall back to default
"""


def test_message_1():
    p = PromptSubclass(PromptSubclass.Type.input, "name")
    assert p.message == "Please provide the 'name'."


def test_message_2():
    p = PromptSubclass(
        PromptSubclass.Type.input,
        name="name",
        message="CUSTOMIZED",
    )
    assert p.message == "CUSTOMIZED"


def test_message_3():
    p = PromptSubclass(
        PromptSubclass.Type.input,
        name="name",
        message="",
    )
    assert p.message == "Please provide the 'name'."
