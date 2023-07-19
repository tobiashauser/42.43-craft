from pathlib import Path

from craft_documents.templates.TemplateManager import TemplateManager
from tests.common.test_common_Configuration import Configuration

test_templates_dir = Path("config.craft").resolve()


def test_initialisation():
    t = TemplateManager(Configuration())
    assert t.folder.path == test_templates_dir

    assert len(t.headers) > 0
    assert "exam" in map(lambda h: h.name, t.headers)
    assert all(map(lambda h: h.extension == ".tex", t.headers))

    assert len(t.exercises) > 0
    assert "intervals" in map(lambda e: e.name, t.exercises)
    assert all(map(lambda e: e.extension == ".tex", t.exercises))

    assert len(t.preambles) > 0
    assert "default" in map(lambda p: p.name, t.preambles)
    assert all(map(lambda p: p.extension == ".tex", t.preambles))
