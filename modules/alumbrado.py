"""CicloRoto: Módulo de Alumbrado.

Conecta reportes PQR con intervenciones de alumbrado público.
"""
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.pipeline import cargar_por_comuna, normalizar_comuna, normalizar_barrio, parse_fecha_mes
from core.trazabilidad import calcular_trazabilidad, calcular_brechas


def cargar_datos():
    """Carga datos PQR y alumbrado."""
    # PQR: 17,643 registros
    pqr = cargar_por_comuna('Cantidad de PQR por comuna', 'pqrs_por_comuna.csv')
    pqr.columns = ['fecha_reporte', 'clase_peticion', 'comuna', 'barrio']
    pqr['comuna'] = pqr['comuna'].apply(normalizar_comuna)
    pqr['barrio'] = pqr['barrio'].apply(normalizar_barrio)
    pqr['periodo'] = pqr['fecha_reporte'].apply(parse_fecha_mes)
    
    # Alumbrado: 253 registros (proyectos ejecutados)
    alum = cargar_por_comuna('Proyectos de alumbrado publico ejecutados', 'alumbrado_publico.csv')
    # El header real está en la fila 1 (la fila 0 es un título)
    alum.columns = ['item', 'proyecto', 'direccion', 'barrio', 'tipo', 'valor_aprobado',
                   'puntos_luminosos', 'comuna', 'proyectos', 'proyectos_especiales']
    alum = alum[alum['comuna'].notna() & alum['comuna'].astype(str).str.contains('comuna|COMUNA|\\d', na=False)]
    alum['comuna'] = alum['comuna'].apply(normalizar_comuna)
    alum['barrio'] = alum['barrio'].apply(normalizar_barrio)
    # Usar 'tipo' como período (algunos tienen fechas)
    alum['periodo'] = alum['tipo'].apply(parse_fecha_mes)
    
    return pqr, alum


def generar_panel(pqr: pd.DataFrame, alum: pd.DataFrame) -> dict:
    """Genera el panel de trazabilidad."""
    # Trazabilidad
    traz = calcular_trazabilidad(pqr, alum)
    brechas = calcular_brechas(traz)
    
    # KPIs
    kpis = {
        'total_pqr': len(pqr),
        'total_intervenciones': len(alum),
        'comunas_con_pqr': pqr['comuna'].nunique(),
        'brechas_identificadas': len(brechas),
        'total_brecha_reportes': int(brechas['total_reportes'].sum()) if len(brechas) > 0 else 0,
    }
    
    return {
        'trazabilidad': traz,
        'brechas': brechas,
        'kpis': kpis,
    }


if __name__ == '__main__':
    print("Cargando datos...")
    pqr, alum = cargar_datos()
    print(f"  PQR: {len(pqr)} registros")
    print(f"  Alumbrado: {len(alum)} registros")
    
    print("\nGenerando panel...")
    panel = generar_panel(pqr, alum)
    print(f"  KPIs: {panel['kpis']}")
    print(f"\n  Brechas identificadas: {len(panel['brechas'])}")
    print(f"\n  Top 5 brechas:")
    print(panel['brechas'].head(5).to_string())
