from pathlib import Path

from draft.common.File import File


class FileImplementation(File):
    def load(self):
        # Assign mock contents
        self._contents = "Hello, world!"


def test_instantiation():
    f = FileImplementation(Path("mock.file"))
    assert f.path == Path("mock.file")
    assert f.contents == "Hello, world!"
    assert f.name == "mock"
    assert f.extension == ".file"
    assert f.parent == Path(".")
