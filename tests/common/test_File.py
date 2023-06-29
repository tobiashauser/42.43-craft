from pathlib import Path

from draft.common.File import File


class FileImplementation(File):
    def load(self):
        # Assign mock contents
        self._contents = "Hello, world!"


def test_instantiation():
    input = FileImplementation(Path())
    assert input.path == Path()
    assert input.contents == "Hello, world!"
