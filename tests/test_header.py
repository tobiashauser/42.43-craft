from pathlib import Path
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
    test_file = Path("test-extract-yaml.tex")
    test_file.touch()
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
    test_file.write_text(input)

    output = Header(test_file).yaml
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
    test_file.write_text(input)

    output = Header(test_file).yaml
    expectation = {'a': ['b', 'c', 'd']}
    assert output == expectation

    test_file.unlink()


def test_extract_placeholders():
    """
    Testing Header.extract_placeholders.

    Expected behaviour:
    Returns a set of the placeholders (no duplicates).
    """
    test_file = Path("test-extract-placeholders.tex")
    test_file.touch()
    input = r"""
\ihead*{\textbf{<<semantic-name>>}\\(<<group>>)}
\chead*{Name:_\rule{0.4\linewidth}{0.4pt}}
\ohead*{\textbf{<<course>>}\\<<place>> • <<semester>>}
\blob{<<group>>}
"""
    test_file.write_text(input)

    output = Header(test_file).placeholders
    expectation = ['course', 'group', 'place', 'semantic-name', 'semester']
    assert sorted(output) == expectation

    test_file.unlink()


def test_create_prompts():
    """
    Testing Header.create_prompts(dict, placeholders)
    -> integration test with both above

    Expected behaviour:
    - Ignore any keys in dict but not in placeholders.
    - Create prompts for all items in placeholders.
    """
    test_file = Path("test-create-prompts.tex")
    test_file.touch()
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
    test_file.write_text(input)

    prompts = Header(test_file).prompts
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

    test_file.unlink()
