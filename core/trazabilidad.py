"""Core: Motor de trazabilidad para CicloRoto.

Conecta reportes (PQR) con intervenciones (alumbrado, malla vial, etc.)
a nivel de Comuna/Barrio + período (mes/año).

Nivel de confianza: MEDIO
- NO afirmamos que una intervención resolvió un reporte específico
- SÍ identificamos patrones: zonas con muchos reportes y pocas intervenciones

Definición de "brecha":
Una brecha de trazabilidad es un registro de reporte (PQR) para el cual
NO se encontró intervención vinculada en las fuentes consultadas, utilizando
los criterios de comparación territorial y temporal definidos.

Esto NO significa que el problema no haya sido resuelto. Significa que,
con los datos públicos disponibles y las reglas de comparación aplicadas,
no fue posible vincular el reporte con una intervención.
"""
import pandas as pd


def calcular_trazabilidad(pqr: pd.DataFrame, intervenciones: pd.DataFrame,
                          col_comuna: str = 'comuna',
                          col_periodo: str = 'periodo') -> pd.DataFrame:
    """Calcula la trazabilidad entre reportes e intervenciones.

    Args:
        pqr: DataFrame con columnas comuna, periodo
        intervenciones: DataFrame con columnas comuna, periodo

    Returns:
        DataFrame con columnas: comuna, periodo, total_reportes,
        total_intervenciones, brecha, nivel_trazabilidad

    Nota:
        - total_reportes: número de PQR en ese comuna/período
        - total_intervenciones: número de intervenciones en ese comuna/período
        - brecha: total_reportes - total_intervenciones
        - nivel_trazabilidad: clasificación de la relación

    Limitaciones:
        - La comparación es a nivel de comuna + período, no dirección exacta
        - Una brecha NO indica problema sin resolver, solo ausencia de
          intervención vinculada en las fuentes consultadas
    """
    # Agregar PQR por comuna + periodo
    pqr_agg = pqr.groupby([col_comuna, col_periodo]).size().reset_index(name='total_reportes')

    # Agregar intervenciones por comuna + periodo
    interv_agg = intervenciones.groupby([col_comuna, col_periodo]).size().reset_index(
        name='total_intervenciones'
    )

    # Merge
    merged = pqr_agg.merge(interv_agg, on=[col_comuna, col_periodo], how='outer').fillna(0)

    # Calcular brecha
    merged['brecha'] = merged['total_reportes'] - merged['total_intervenciones']

    # Nivel de trazabilidad
    def nivel_trazabilidad(row):
        if row['total_intervenciones'] == 0 and row['total_reportes'] > 0:
            return 'Sin intervención vinculada'
        elif row['brecha'] > row['total_intervenciones']:
            return 'Intervención insuficiente'
        elif row['brecha'] <= 0:
            return 'Intervención suficiente'
        else:
            return 'Intervención parcial'

    merged['nivel_trazabilidad'] = merged.apply(nivel_trazabilidad, axis=1)

    return merged.sort_values(['comuna', 'periodo'])


def calcular_brechas(trazabilidad: pd.DataFrame) -> pd.DataFrame:
    """Identifica brechas de trazabilidad.

    Una brecha es un registro donde existen reportes pero no se encontró
    intervención vinculada en las fuentes consultadas.

    Returns:
        DataFrame con registros sin intervención vinculada, ordenados por
        número de reportes (descendente).

    Nota:
        - Estas brechas NO indican problemas sin resolver
        - Indican ausencia de intervención vinculada en las fuentes analizadas
    """
    brechas = trazabilidad[trazabilidad['nivel_trazabilidad'] == 'Sin intervención vinculada']
    return brechas.sort_values('total_reportes', ascending=False)


def generar_resumen_metodologico() -> str:
    """Genera resumen metodológico para documentación."""
    return """
Resumen metodológico:
- Fuentes: PQR (17,642 registros) y Alumbrado público (247 registros de 2017)
- Fecha de consulta: 2026-10-19
- Criterio de comparación: Comuna + Período (mes/año)
- Nivel de confianza: MEDIO

Limitaciones:
- La comparación es a nivel de comuna + período, no dirección exacta
- Una PQR sin coincidencia NO demuestra que el problema continúe sin resolver
- Una coincidencia territorial y temporal NO demuestra causalidad
- La cobertura y calidad de los registros puede variar entre años
- Los resultados dependen de las fuentes disponibles y reglas aplicadas

Interpretación correcta:
- "Sin intervención vinculada" = no se encontró intervención en las fuentes consultadas
- NO significa "problema sin resolver"
"""
