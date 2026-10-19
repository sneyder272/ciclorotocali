"""Core: Motor de trazabilidad para CicloRoto.

Conecta reportes (PQR) con intervenciones (alumbrado, malla vial, etc.)
a nivel de Comuna/Barrio + período (mes/año).

Nivel de confianza: MEDIO
- NO afirmamos que una intervención resolvió un reporte específico
- SÍ identificamos patrones: zonas con muchos reportes y pocas intervenciones
"""
import pandas as pd

def calcular_trazabilidad(pqr: pd.DataFrame, intervenciones: pd.DataFrame,
                          col_comuna: str = 'comuna',
                          col_barrio: str = 'barrio',
                          col_periodo: str = 'periodo') -> pd.DataFrame:
    """Calcula la trazabilidad entre reportes e intervenciones.
    
    Returns:
        DataFrame con columnas: comuna, periodo, total_reportes, total_intervenciones,
        brecha (reportes - intervenciones), nivel_trazabilidad
    """
    # Agregar PQR por comuna + periodo
    pqr_agg = pqr.groupby([col_comuna, col_periodo]).size().reset_index(name='total_reportes')
    
    # Agregar intervenciones por comuna + periodo
    interv_agg = intervenciones.groupby([col_comuna, col_periodo]).size().reset_index(name='total_intervenciones')
    
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
    """Identifica brechas verificables: zonas con reportes pero sin intervención."""
    brechas = trazabilidad[trazabilidad['nivel_trazabilidad'] == 'Sin intervención vinculada']
    return brechas.sort_values('total_reportes', ascending=False)
