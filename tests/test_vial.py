"""Pruebas del módulo vial y de la interfaz."""
from pathlib import Path

import pandas as pd

from modules.vial import (
    canonicalizar_cruce,
    cargar_datos,
    generar_ficha,
    generar_panel,
)

APP = Path(__file__).resolve().parent.parent / 'app.py'


def test_canonicalizar_variantes_del_mismo_cruce():
    esperado = 'CALLE 70 CON CARRERA 8'
    assert canonicalizar_cruce('Calle 70 con Carrera 8') == esperado
    assert canonicalizar_cruce('CRA 8 CON CL 70') == esperado
    assert canonicalizar_cruce('CARRERA 8 & CALLE 70') == esperado
    assert canonicalizar_cruce('calle 70 carrera 8') == esperado


def test_canonicalizar_formatos_sin_conector():
    assert canonicalizar_cruce('CALLE 25 CARRERA 109') == (
        'CALLE 25 CON CARRERA 109'
    )
    assert canonicalizar_cruce('CALLE 70  &  CARRERA 3') == (
        'CALLE 70 CON CARRERA 3'
    )


def test_no_inventa_cruces():
    assert canonicalizar_cruce('CLINICA CALI') is None
    assert canonicalizar_cruce('.') is None
    assert canonicalizar_cruce('') is None
    assert canonicalizar_cruce('CALLE 5') is None


def test_cargar_datos():
    df = cargar_datos()
    assert len(df) == 51236
    assert df['moto'].dtype == bool
    assert df['cruce'].notna().sum() == 28411
    assert df['cruce'].nunique() == 9261


def test_ranking_consolida_y_ordena():
    df = cargar_datos()
    panel = generar_panel(df, min_registros=5)
    ranking = panel['ranking']
    assert not ranking.empty
    assert ranking.iloc[0]['cruce'] == 'CALLE 70 CON CARRERA 8'
    assert ranking.iloc[0]['registros'] == 148
    assert ranking['tasa_ajustada'].is_monotonic_decreasing
    assert ranking['ic_inferior'].le(ranking['tasa_ajustada']).all()
    assert ranking.iloc[0]['ventana_pico'].endswith(':59')


def test_filtro_por_anio():
    df = cargar_datos()
    panel = generar_panel(df, anio=2024)
    assert panel['kpis']['total_registros'] == 4126
    assert not panel['ranking'].empty


def test_ficha_incluye_solicitud_sin_afirmar_causalidad():
    df = cargar_datos()
    cruce = generar_panel(df, min_registros=5)['ranking'].iloc[0]['cruce']
    detalle = df[df['cruce'] == cruce]
    ficha = generar_ficha(detalle, cruce)

    assert cruce.title().replace(' Con ', ' con ') in ficha
    assert 'Ley 1755' in ficha
    assert '148' in ficha
    assert 'no se afirma que falte una obra' in ficha.lower()


def test_filtro_sin_datos_no_falla():
    df = cargar_datos()
    panel = generar_panel(df, anio=2019)
    assert panel['ranking'].empty
    assert panel['kpis']['total_registros'] == 5974


def test_app_renderiza_y_busca():
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(APP), default_timeout=120).run()
    assert len(at.exception) == 0, [e.value for e in at.exception]
    assert len(at.tabs) == 4

    etiquetas = {m.label for m in at.metric}
    assert 'Siniestros con lesionados' in etiquetas
    assert 'Cruces con obra verificable' in etiquetas

    at.text_input[0].set_value('calle 70 con carrera 8').run()
    assert len(at.exception) == 0, [e.value for e in at.exception]
    etiquetas = {m.label for m in at.metric}
    assert 'Registros históricos' in etiquetas
