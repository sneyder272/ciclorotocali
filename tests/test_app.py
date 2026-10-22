"""Prueba de humo: la interfaz debe renderizar sin excepciones."""
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parent.parent / 'app.py'


def test_app_renderiza_sin_excepciones():
    at = AppTest.from_file(str(APP), default_timeout=90).run()
    assert len(at.exception) == 0, [e.value for e in at.exception]
    assert len(at.tabs) == 4
    etiquetas = {m.label for m in at.metric}
    assert 'Reportes vinculables' in etiquetas
    assert 'Proyectos de alumbrado (2017)' in etiquetas
