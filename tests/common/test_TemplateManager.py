from pathlib import Path

from draft.common.TemplateManager import TemplateManager
from tests.common.test_Configuration import Configuration

test_templates_dir = Path("config.draft")


def test_initialisation():
    t = TemplateManager(Configuration())
    assert t.folder.path == test_templates_dir

    assert len(t.headers) > 0
    assert "exam" in map(lambda h: h.name, t.headers)
    assert all(map(lambda h: h.extension == ".tex", t.headers))

    assert len(t.exercises) > 0
    assert "intervals" in map(lambda e: e.name, t.exercises)
    assert all(map(lambda e: e.extension == ".tex", t.exercises))
