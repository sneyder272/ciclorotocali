"""Core: Pipeline de datos para CicloRoto."""
import pandas as pd
from pathlib import Path
import requests

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

def descargar_csv(url: str, nombre: str, timeout: int = 60) -> pd.DataFrame:
    """Descarga un CSV desde URL y lo guarda localmente."""
    path = RAW_DIR / nombre
    if path.exists():
        return pd.read_csv(path, encoding='utf-8-sig', low_memory=False)
    
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    
    # Detectar encoding
    for enc in ['utf-8-sig', 'latin-1']:
        try:
            txt = r.content.decode(enc)
            break
        except:
            continue
    
    # Detectar separador
    sep = ';' if txt.count(';') > txt.count(',') else ','
    
    # Guardar
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(r.content)
    
    return pd.read_csv(path, encoding=enc, sep=sep, low_memory=False)

def cargar_por_comuna(query: str, nombre: str) -> pd.DataFrame:
    """Busca un dataset por query y descarga su primer CSV."""
    r = requests.get('https://datos.cali.gov.co/api/3/action/package_search',
                     params={'q': query, 'rows': 1}, timeout=30)
    d = r.json()['result']
    if not d['count']:
        raise ValueError(f"No se encontró: {query}")
    pkg = d['results'][0]
    for res in pkg.get('resources', []):
        if (res.get('format') or '').upper() == 'CSV':
            return descargar_csv(res['url'], nombre)
    raise ValueError(f"Sin CSV: {query}")

def normalizar_comuna(val) -> str:
    """Normaliza comuna a formato consistente."""
    if pd.isna(val):
        return "N/D"
    val = str(val).strip()
    if val.upper() in ('N/D', 'N/A', '', 'NAN'):
        return "N/D"
    return val

def normalizar_barrio(val) -> str:
    """Normaliza barrio a mayúsculas."""
    if pd.isna(val):
        return "N/D"
    val = str(val).strip().upper()
    if val in ('N/D', 'N/A', '', 'NAN'):
        return "N/D"
    return val

def parse_fecha_mes(val):
    """Parsea fechas a período mes/año."""
    if pd.isna(val):
        return None
    val = str(val).strip()
    # Formatos comunes: "01/01/2024", "ene-24", "2024-01", "2024"
    try:
        # Intentar formato dd/mm/yyyy
        if '/' in val:
            parts = val.split('/')
            if len(parts) == 3:
                return f"{parts[2]}-{parts[1].zfill(2)}"
        # Intentar formato mes-año (ene-24)
        meses = {'ene': '01', 'feb': '02', 'mar': '03', 'abr': '04', 'may': '05', 'jun': '06',
                 'jul': '07', 'ago': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dic': '12'}
        for mes_nom, mes_num in meses.items():
            if val.lower().startswith(mes_nom):
                parts = val.split('-')
                if len(parts) == 2:
                    anio = parts[1]
                    if len(anio) == 2:
                        anio = '20' + anio
                    return f"{anio}-{mes_num}"
        # Si es solo año
        if val.isdigit() and len(val) == 4:
            return f"{val}-01"
    except:
        pass
    return None
