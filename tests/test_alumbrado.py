"""Tests del núcleo y del módulo de alumbrado."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.pipeline import normalizar_comuna, normalizar_barrio, parse_fecha_mes
from core.trazabilidad import calcular_trazabilidad, calcular_brechas
from modules.alumbrado import (
    PERIODO_ALUMBRADO,
    cargar_datos,
    generar_panel,
)


def test_normalizar_comuna():
    assert normalizar_comuna("1") == "Comuna 1"
    assert normalizar_comuna("Comuna 01") == "Comuna 1"
    assert normalizar_comuna("COMUNA 20") == "Comuna 20"
    assert normalizar_comuna("  comuna 13 ") == "Comuna 13"
    assert normalizar_comuna("N/D") == "N/D"
    assert normalizar_comuna(None) == "N/D"
    assert normalizar_comuna("23") == "N/D"


def test_normalizar_barrio():
    assert normalizar_barrio("Centenario") == "CENTENARIO"
    assert normalizar_barrio("  Colinas   del Sur ") == "COLINAS DEL SUR"
    assert normalizar_barrio("N/D") == "N/D"
    assert normalizar_barrio(None) == "N/D"


def test_parse_fecha_mes():
    assert parse_fecha_mes("01/01/2024") == "2024-01"
    assert parse_fecha_mes("30/11/2025") == "2025-11"
    assert parse_fecha_mes("ene-24") == "2024-01"
    assert parse_fecha_mes("2024") == "2024-01"
    # Fechas imposibles o fuera del rango documentado se descartan
    assert parse_fecha_mes("31/13/2024") is None
    assert parse_fecha_mes("01/01/2028") is None
    assert parse_fecha_mes("05/05/2205") is None
    assert parse_fecha_mes(None) is None


def test_calcular_trazabilidad():
    pqr = pd.DataFrame({
        'comuna': ['1', '1', '2'],
        'periodo': ['2024-01', '2024-02', '2024-01'],
        'barrio': ['A', 'B', 'C'],
    })
    interv = pd.DataFrame({
        'comuna': ['1'],
        'periodo': ['2024-01'],
        'barrio': ['A'],
    })
    result = calcular_trazabilidad(pqr, interv)
    assert len(result) == 3
    assert 'brecha' in result.columns
    # La comuna 1 en 2024-01 tiene una intervención; no debe ser brecha
    fila = result[(result['comuna'] == '1') & (result['periodo'] == '2024-01')]
    assert fila['total_intervenciones'].iloc[0] == 1


def test_calcular_brechas():
    pqr = pd.DataFrame({
        'comuna': ['1', '1', '2', '2', '2'],
        'periodo': ['2024-01', '2024-01', '2024-01', '2024-02', '2024-02'],
        'barrio': ['A', 'B', 'C', 'D', 'E'],
    })
    interv = pd.DataFrame({
        'comuna': ['1'],
        'periodo': ['2024-01'],
        'barrio': ['A'],
    })
    traz = calcular_trazabilidad(pqr, interv)
    brechas = calcular_brechas(traz)
    assert len(brechas) > 0
    assert 'total_reportes' in brechas.columns


def test_alumbrado_usa_el_anio_del_archivo():
    """Regresión: el período no debe derivarse de la columna 'tipo'."""
    _, alum = cargar_datos()
    assert len(alum) > 0
    assert set(alum['periodo'].unique()) == {PERIODO_ALUMBRADO}


def test_no_se_inventa_un_cruce_inexistente():
    """Con estas fuentes el número de reportes vinculables debe ser cero."""
    pqr, alum = cargar_datos()
    panel = generar_panel(pqr, alum)
    assert panel['kpis']['vinculables'] == 0
    temporal = panel['diagnostico'].query("criterio == 'Solapamiento temporal'")
    assert temporal['estado'].iloc[0] == 'No'
