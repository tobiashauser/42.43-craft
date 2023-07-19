from pathlib import Path

from craft_documents.common.File import File


class FileImplementation(File):
    def load(self):
        # Assign mock contents
        self._contents = "Hello, world!"


def test_instantiation():
    f = FileImplementation(Path("mock.file"))
    assert "mock.file" in str(f.path)
    assert f.contents == "Hello, world!"
    assert f.name == "mock"
    assert f.extension == ".file"
