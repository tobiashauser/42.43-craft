import pytest
from draft.models.headers import Header


def test_extract_yaml():
    r"""
    Testing Header.extract_yaml().

    Expected behaviour:
    Extract multiple yaml blocks enclosed in '\iffalse' and '\fi' which
    are accumulated into one dictionary. Blocks at the top of the file
    take precedence over blocks further down. List values are accumulated.
    """
    input = r"""
\iffalse
a:
    b: c
\fi
\iffalse
d: e
\fi
\iffalse
a:
    f: g
\fi
"""
    output = Header.extract_yaml(input)
    expectation = {'a': {'b': 'c'}, 'd': 'e'}
    assert output == expectation

    # test list accumulation
    input = r"""
\iffalse
a:
- b
\fi
\iffalse
a:
- c
\fi
\iffalse
a: d
\fi
"""
    output = Header.extract_yaml(input)
    expectation = {'a': ['b', 'c', 'd']}
    assert output == expectation


def test_extract_placeholders():
    """
    Testing Header.extract_placeholders.

    Expected behaviour:
    Returns a set of the placeholders (no duplicates).
    """
    input = r"""
\ihead*{\textbf{<<semantic-name>>}\\(<<group>>)}
\chead*{Name:_\rule{0.4\linewidth}{0.4pt}}
\ohead*{\textbf{<<course>>}\\<<place>> • <<semester>>}
\blob{<<group>>}
"""
    output = Header.extract_placeholders(input)
    expectation = ['course', 'group', 'place', 'semantic-name', 'semester']
    assert sorted(output) == expectation


def test_create_prompts():
    """
    Testing Header.create_prompts(dict, placeholders)
    -> integration test with both above

    Expected behaviour:
    - Ignore any keys in dict but not in placeholders.
    - Create prompts for all items in placeholders.
    """
    input = r"""
\iffalse
prompts:
- semantic-name:
    type: input
    message: Hello, world!
    default: Blob
\fi
\ihead*{\textbf{<<semantic-name>>}\\(<<group>>)}
\blob{<<group>>}
"""
    prompts = Header.create_prompts(
        Header.extract_yaml(input)['prompts'],
        Header.extract_placeholders(input)
    )
    expectation = [
        {
            'type': 'input',
            'name': 'semantic-name',
            'message': 'Hello, world!',
            'default': 'Blob',
        },
        {
            'type': 'input',
            'name': 'group',
            'message': 'Please provide the group.',
        },
    ]
    assert prompts == expectation
