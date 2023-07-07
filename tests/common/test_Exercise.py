from pathlib import Path

from draft.common.Exercise import Exercise as LiveExercise
from tests.common.test_Configuration import Configuration

test_folder = Path("tests/test_Folder")
tex = test_folder / "intervals.tex"
ly = test_folder / "intervals.ly"

exercise_contents = r"""
\iffalse
supplements: intervals.ly
\fi
"""


def setup_test_folder():
    test_folder.mkdir(exist_ok=True)
    tex.touch(exist_ok=True)
    ly.touch(exist_ok=True)

    tex.write_text(exercise_contents)


def teardown_test_folder():
    ly.unlink(missing_ok=True)
    tex.unlink(missing_ok=True)
    test_folder.rmdir()


def test_instantiation():
    setup_test_folder()

    e = LiveExercise(tex, Configuration())
    assert e.path == tex
    assert e.contents == exercise_contents
    assert e.name == tex.stem
    assert e.extension == tex.suffix
    assert e.parent == test_folder
    assert len(e.supplements) == 1
    assert e.supplements[0].path == ly

    teardown_test_folder()
