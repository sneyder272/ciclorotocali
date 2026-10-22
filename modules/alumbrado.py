"""CicloRoto: módulo de alumbrado público.

Fuentes
-------
PQR   : reportes ciudadanos 2024-2025 por comuna y barrio.
        No incluye una categoría temática que permita aislar alumbrado.
Alumbrado: 251 proyectos ejecutados en 2017. El año aparece únicamente en
        el título del archivo; no hay fecha por registro ni identificador
        de caso.

Hallazgo del módulo
-------------------
No es posible vincular un reporte con una intervención de alumbrado:
- las fuentes no comparten clave (PQR usa 'Comuna 20', alumbrado usa '20');
- no hay solapamiento temporal (2024-2025 frente a 2017);
- el alumbrado no tiene fecha por registro ni número de caso;
- la PQR no tiene categoría temática de alumbrado.

El módulo no inventa un cruce: cuantifica la brecha documental y describe
la cobertura territorial de ambas fuentes.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.pipeline import (
    cargar_por_comuna,
    normalizar_barrio,
    normalizar_comuna,
    parse_fecha_mes,
)

PERIODO_ALUMBRADO = '2017'
COLUMNAS_PQR = ['fecha_reporte', 'clase_peticion', 'comuna', 'barrio']
COLUMNAS_ALUMBRADO = [
    'item', 'proyecto', 'direccion', 'barrio', 'tipo', 'valor_aprobado',
    'puntos_luminosos', 'comuna', 'proyectos', 'proyectos_especiales',
]


def cargar_datos():
    """Carga y normaliza PQR y proyectos de alumbrado."""
    pqr = cargar_por_comuna('Cantidad de PQR por comuna', 'pqrs_por_comuna.csv')
    pqr.columns = COLUMNAS_PQR
    pqr['comuna'] = pqr['comuna'].apply(normalizar_comuna)
    pqr['barrio'] = pqr['barrio'].apply(normalizar_barrio)
    pqr['periodo'] = pqr['fecha_reporte'].apply(parse_fecha_mes)
    pqr['anio'] = pqr['periodo'].str[:4]

    # La primera fila del CSV es un título ("... AÑO 2017"); el encabezado
    # real está en la segunda fila.
    alum = cargar_por_comuna(
        'Proyectos de alumbrado publico ejecutados',
        'alumbrado_publico.csv',
        skiprows=1,
    )
    alum.columns = COLUMNAS_ALUMBRADO
    alum['comuna'] = alum['comuna'].apply(normalizar_comuna)
    alum['barrio'] = alum['barrio'].apply(normalizar_barrio)
    alum['valor_aprobado'] = pd.to_numeric(alum['valor_aprobado'], errors='coerce')
    alum['puntos_luminosos'] = pd.to_numeric(alum['puntos_luminosos'], errors='coerce')
    # Año documentado en el título del archivo, no inferido de otra columna.
    alum['periodo'] = PERIODO_ALUMBRADO
    alum = alum[alum['comuna'] != 'N/D'].reset_index(drop=True)

    return pqr, alum


def _diagnostico(pqr: pd.DataFrame, alum: pd.DataFrame) -> pd.DataFrame:
    """Evalúa si las fuentes permiten vincular reportes e intervenciones."""
    periodos_pqr = set(pqr['periodo'].dropna().unique())
    periodos_alum = set(alum['periodo'].dropna().unique())
    solapamiento = sorted(periodos_pqr & periodos_alum)

    filas = [
        {
            'criterio': 'Clave territorial común',
            'estado': 'Parcial',
            'detalle': 'Normalizable a Comuna 1-22, pero no hay clave de caso.',
            'bloqueante': 'No',
        },
        {
            'criterio': 'Solapamiento temporal',
            'estado': 'No',
            'detalle': (
                f'PQR {min(periodos_pqr)} a {max(periodos_pqr)}; '
                f'alumbrado {PERIODO_ALUMBRADO}. '
                f'Meses en común: {len(solapamiento)}.'
            ),
            'bloqueante': 'Sí',
        },
        {
            'criterio': 'Fecha por registro en alumbrado',
            'estado': 'No',
            'detalle': 'Solo el año figura en el título del archivo.',
            'bloqueante': 'Sí',
        },
        {
            'criterio': 'Categoría temática en PQR',
            'estado': 'No',
            'detalle': 'Las clases son Pqr, Cita médica, Denuncia, etc.; '
                       'ninguna identifica alumbrado.',
            'bloqueante': 'Sí',
        },
        {
            'criterio': 'Identificador de caso',
            'estado': 'No',
            'detalle': 'Ninguna de las dos fuentes publica un número de caso.',
            'bloqueante': 'Sí',
        },
    ]
    return pd.DataFrame(filas)


def _calidad(pqr: pd.DataFrame, alum: pd.DataFrame) -> pd.DataFrame:
    """Métricas de calidad y cobertura de las fuentes."""
    total_pqr = len(pqr)
    sin_fecha = int(pqr['periodo'].isna().sum())
    sin_comuna = int((pqr['comuna'] == 'N/D').sum())

    total_alum = len(alum)
    comunas_alum = int(alum['comuna'].nunique())

    filas = [
        ('PQR sin período válido', sin_fecha,
         'Fecha ausente o fuera de 2024-2025.'),
        ('PQR sin comuna', sin_comuna,
         f'{100 * sin_comuna / total_pqr:.1f}% del total.'),
        ('Comunas distintas en PQR', int(pqr['comuna'].nunique()) - 1,
         'Tras normalizar; Cali tiene 22 comunas.'),
        ('Proyectos de alumbrado', total_alum,
         'Filas con comuna válida.'),
        ('Comunas con proyectos', comunas_alum,
         'El archivo no cubre las 22 comunas.'),
        ('Proyectos sin puntos luminosos', int(alum['puntos_luminosos'].isna().sum()),
         'Dato faltante en la fuente original.'),
    ]
    return pd.DataFrame(filas, columns=['métrica', 'valor', 'nota'])


def generar_panel(pqr: pd.DataFrame, alum: pd.DataFrame) -> dict:
    """Genera el panel de diagnóstico, cobertura y calidad."""
    cobertura = (
        pqr[pqr['comuna'] != 'N/D']
        .groupby('comuna')
        .size()
        .rename('reportes_2024_2025')
        .reset_index()
        .merge(
            alum.groupby('comuna').agg(
                proyectos_2017=('item', 'count'),
                puntos_luminosos=('puntos_luminosos', 'sum'),
                inversion_cop=('valor_aprobado', 'sum'),
            ).reset_index(),
            on='comuna',
            how='outer',
        )
        .fillna(0)
        .sort_values('reportes_2024_2025', ascending=False)
        .reset_index(drop=True)
    )
    cobertura['proyectos_2017'] = cobertura['proyectos_2017'].astype(int)
    cobertura['reportes_2024_2025'] = cobertura['reportes_2024_2025'].astype(int)
    cobertura['tiene_proyecto_2017'] = cobertura['proyectos_2017'] > 0

    kpis = {
        'total_pqr': len(pqr),
        'pqr_2024': int((pqr['anio'] == '2024').sum()),
        'pqr_2025': int((pqr['anio'] == '2025').sum()),
        'total_intervenciones': len(alum),
        'puntos_luminosos': int(alum['puntos_luminosos'].sum()),
        'inversion_cop': int(alum['valor_aprobado'].sum()),
        'comunas_con_proyectos': int(alum['comuna'].nunique()),
        'pqr_sin_comuna': int((pqr['comuna'] == 'N/D').sum()),
        'vinculables': 0,
    }

    return {
        'kpis': kpis,
        'diagnostico': _diagnostico(pqr, alum),
        'cobertura': cobertura,
        'calidad': _calidad(pqr, alum),
    }


if __name__ == '__main__':
    print('Cargando datos...')
    pqr, alum = cargar_datos()
    panel = generar_panel(pqr, alum)
    print(f"  PQR: {len(pqr):,} | Alumbrado: {len(alum):,}")
    print(f"  KPIs: {panel['kpis']}")
    print()
    print(panel['diagnostico'].to_string(index=False))
