"""Tests del módulo de alumbrado."""
import pytest
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.pipeline import normalizar_comuna, normalizar_barrio, parse_fecha_mes
from core.trazabilidad import calcular_trazabilidad, calcular_brechas


def test_normalizar_comuna():
    assert normalizar_comuna("1") == "1"
    assert normalizar_comuna("Comuna 01") == "Comuna 01"
    assert normalizar_comuna("N/D") == "N/D"
    assert normalizar_comuna(None) == "N/D"


def test_normalizar_barrio():
    assert normalizar_barrio("Centenario") == "CENTENARIO"
    assert normalizar_barrio("N/D") == "N/D"
    assert normalizar_barrio(None) == "N/D"


def test_parse_fecha_mes():
    assert parse_fecha_mes("01/01/2024") == "2024-01"
    assert parse_fecha_mes("ene-24") == "2024-01"
    assert parse_fecha_mes("2024") == "2024-01"
    assert parse_fecha_mes(None) is None


def test_calcular_trazabilidad():
    pqr = pd.DataFrame({
        'comuna': ['1', '1', '2'],
        'periodo': ['2024-01', '2024-02', '2024-01'],
        'barrio': ['A', 'B', 'C']
    })
    interv = pd.DataFrame({
        'comuna': ['1'],
        'periodo': ['2024-01'],
        'barrio': ['A']
    })
    result = calcular_trazabilidad(pqr, interv)
    assert len(result) == 3
    assert 'brecha' in result.columns


def test_calcular_brechas():
    pqr = pd.DataFrame({
        'comuna': ['1', '1', '2', '2', '2'],
        'periodo': ['2024-01', '2024-01', '2024-01', '2024-02', '2024-02'],
        'barrio': ['A', 'B', 'C', 'D', 'E']
    })
    interv = pd.DataFrame({
        'comuna': ['1'],
        'periodo': ['2024-01'],
        'barrio': ['A']
    })
    traz = calcular_trazabilidad(pqr, interv)
    brechas = calcular_brechas(traz)
    assert len(brechas) > 0
    assert 'total_reportes' in brechas.columns
