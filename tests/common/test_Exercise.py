from pathlib import Path

from draft.common.Exercise import Exercise as LiveExercise
from draft.configuration.Configuration import Configuration
from tests.common.test_common_Configuration import Configuration

test_folder = Path("tests/test_Folder")
tex = test_folder / "intervals.tex"
ly = test_folder / "intervals.ly"

exercise_contents = r"""
\iffalse
supplements: 
    - intervals.ly
\fi
"""


class ExerciseTest(LiveExercise):
    def __init__(self, configuration: Configuration = Configuration()):
        super().__init__(Path("exercise.tex"), configuration)

    def load(self):
        self._contents = exercise_contents


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
    c = Configuration()

    e = LiveExercise(tex, c)
    assert str(tex) in str(e.path)
    # assert e.contents == exercise_contents
    assert e.name == tex.stem
    assert e.extension == tex.suffix
    assert str(test_folder) in str(e.parent)
    assert len(e.supplements) == 1
    assert str(ly) in str(e.supplements[0].path)

    teardown_test_folder()
