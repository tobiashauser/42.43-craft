from pathlib import Path

from draft.common.Template import Template

contents = r"""
This is a template for a <<course>>. It is
written by <<author>>. 

\iffalse
course:
    name: blob
    type: input
    validate: "lambda v: len(v) != 0"
\fi

What if a placeholder is customized but not as a dictionary?
It doesn't do anything.

\iffalse
author: E.A.P.
\fi
"""


class TemplateImplementation(Template):
    def __init__(
        self,
        path: Path = Path(),
    ):
        super().__init__(
            path=path,
            placeholder_prefix=r"<<",
            placeholder_suffix=r">>",
            yaml_prefix=r"\\iffalse",
            yaml_suffix=r"\\fi",
        )

    def load(self):
        self._contents = contents


def test_instantiation():
    input = TemplateImplementation()
    assert input.contents == contents


def test_handlebars():
    input = TemplateImplementation()
    assert input.placeholders == set(["course", "author"])


def test_yaml():
    input = TemplateImplementation()
    expectation = {
        "course": {
            "name": "blob",
            "type": "input",
            "validate": "lambda v: len(v) != 0",
        },
        "author": "E.A.P.",
    }

    assert input.yaml == expectation


def test_prompts():
    input = TemplateImplementation()
    expectation = [
        {
            "name": "author",
            "type": "input",
            "message": "Please provide the 'author'.",
        },
        {
            "name": "course",  # was customized in YAML -> should be ignored
            "type": "input",
            "message": "Please provide the 'course'.",
            "validate": lambda v: len(v) != 0,  # functions are not equatable...
        },
    ]
    prompts = sorted(input.prompts, key=lambda d: d["name"])
    assert len(prompts) == 2
    assert prompts[0] == expectation[0]
    assert prompts[1]["name"] == "course"
    assert prompts[1]["type"] == "input"
    assert prompts[1]["message"] == "Please provide the 'course'."
    assert "validate" in prompts[1]
