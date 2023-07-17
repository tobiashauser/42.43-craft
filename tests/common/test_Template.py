from pathlib import Path

from draft.common.helpers import combine_dictionaries
from draft.common.Template import Template
from draft.configuration.Configuration import Configuration as LiveConfiguration
from tests.common.test_common_Configuration import Configuration

contents = r"""
This is a template for a <<course>>. It is
written by <<author>>.

\iffalse
course:
    name: blob
    type: input
    validate: "lambda v: len(v) != 0"
    when: "lambda d: 'name' not in d"
\fi

% This is a comment.

What if a placeholder is customized but not as a dictionary?
It doesn't do anything.

\iffalse
author: E.A.P.
\fi
"""


class TemplateImplementation(Template):
    def __init__(
        self,
        configuration: Configuration = Configuration(),
        path: Path = Path("jane.tex"),
    ):
        super().__init__(configuration=configuration, path=path)

    def load(self):
        self._contents = contents


def test_instantiation():
    t = TemplateImplementation()
    assert t.contents == contents
    assert t.configuration == Configuration()
    assert t.placeholder_prefix == "<<"
    assert t.placeholder_suffix == ">>"
    assert t.single_line_comment_prefix == r"%"
    assert t.block_comment_prefix == r"\\iffalse"
    assert t.block_comment_suffix == r"\\fi"


def test_placeholders():
    input = TemplateImplementation()
    assert input.placeholders == set(["course", "author"])


def test_yaml():
    input = TemplateImplementation()
    expectation = {
        "course": {
            "name": "blob",
            "type": "input",
            "validate": "lambda v: len(v) != 0",
            "when": "lambda d: 'name' not in d",
        },
        "author": "E.A.P.",
    }

    assert input.yaml == expectation


def test_prompts():
    input = TemplateImplementation(
        configuration=Configuration(allow_eval=True, year=2023)
    )
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

    assert prompts[0]["name"] == "author"
    assert prompts[0]["type"] == "input"
    assert prompts[0]["message"] == "Please provide the 'author'."
    assert "validate" not in prompts[0]
    # assert "when" in prompts[0]
    assert len(prompts[0]) == 3

    assert prompts[1]["name"] == "course"
    assert prompts[1]["type"] == "input"
    assert prompts[1]["message"] == "Please provide the 'course'."
    assert "validate" in prompts[1]
    # assert "when" in prompts[1]
    assert len(prompts[1]) == 5


def test_prompts_allow_eval_configuration():
    t = TemplateImplementation(configuration=Configuration(allow_eval=False))
    prompts = sorted(t.prompts, key=lambda d: d["name"])
    assert "validate" not in prompts[1]
    # assert "when" in prompts[1]

    t = TemplateImplementation(configuration=Configuration(allow_eval=True))
    prompts = sorted(t.prompts, key=lambda d: d["name"])
    assert "validate" in prompts[1]
    # assert "when" in prompts[1]


def test_reference_semantics_of_configuration():
    c = Configuration()
    t1 = TemplateImplementation(configuration=c)
    t2 = TemplateImplementation(configuration=c)

    assert t1.configuration == t2.configuration

    t1.configuration["A"] = 1
    assert t2.configuration["A"] == 1
    assert t1.configuration == t2.configuration


def test_remove_comments():
    t = TemplateImplementation(Configuration(remove_comments=True))
    assert (
        t.contents
        == """
This is a template for a <<course>>. It is
written by <<author>>.

What if a placeholder is customized but not as a dictionary?
It doesn't do anything.

"""
    )


def test_tokens_not_present():
    test_file = Path("tests/test_tokens_not_present.INVALID")

    with test_file.open("w") as file:
        file.write(contents)

    try:
        t = Template(Configuration(), test_file)  # this line throws an exception
    except Exception:
        assert True

    test_file.unlink()


def test_set_placeholders():
    t = TemplateImplementation()
    t.set_placeholders(t.configuration)

    assert t.contents == contents
    assert t.placeholders == {"author", "course"}

    t._configuration = Configuration(author="TH")
    t.set_placeholders(t.configuration)
    assert not t.contents == contents
    assert t.placeholders == {"course"}
