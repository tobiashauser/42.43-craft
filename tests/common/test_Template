from pathlib import Path

from draft.common.Template import Template as LiveTemplate


class Template(LiveTemplate):
    def load(self):
        self._contents = "Hello, world!"


def test_instantiation():
    input = Template(path=Path())
    assert input.contents == "Hello, world!"
