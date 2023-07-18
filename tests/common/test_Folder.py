from pathlib import Path

from craft_documents.common.Folder import Folder


class LiveFolderImplementation(Folder):
    pass


def test_instantiation():
    test_folder = Path("tests/test_folder_instantiation")
    test_folder.mkdir(exist_ok=True)

    one = test_folder / "01.md"
    one.touch(exist_ok=True)
    two = test_folder / "02.tex"
    two.touch(exist_ok=True)
    three = test_folder / "03"
    three.mkdir(exist_ok=True)

    f = LiveFolderImplementation(test_folder)
    assert f.name == "test_folder_instantiation"
    # assert f.subfiles == [two, one]
    # assert f.subfolders == [three]

    one.unlink(missing_ok=True)
    two.unlink(missing_ok=True)
    three.rmdir()
    test_folder.rmdir()
