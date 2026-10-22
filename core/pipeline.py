"""Core: pipeline de datos de CicloRoto.

Responsabilidades:
- Leer los CSV locales sin depender de la red.
- Normalizar comunas, barrios y fechas de forma verificable.
- Descargar desde CKAN solo si el archivo local no existe.
"""
import io
import re
from pathlib import Path

import pandas as pd
import requests

RAW_DIR = Path(__file__).resolve().parent.parent / 'data' / 'raw'
PROCESSED_DIR = Path(__file__).resolve().parent.parent / 'data' / 'processed'
CKAN_API = 'https://datos.cali.gov.co/api/3/action/package_search'

# Rango observado en la fuente PQR. Las fechas fuera de este rango se
# consideran inválidas y se excluyen de los períodos (ver docs/audit.md).
ANIO_MIN = 2024
ANIO_MAX = 2025


def leer_csv_local(nombre: str, skiprows: int = 0) -> pd.DataFrame:
    """Lee un CSV de data/raw detectando encoding y separador.

    No usa la red. Si el archivo no existe, lanza FileNotFoundError.
    """
    path = RAW_DIR / nombre
    if not path.exists():
        raise FileNotFoundError(
            f"No existe {path}. Ejecuta la descarga o copia el CSV en data/raw/."
        )

    raw = path.read_bytes()
    for enc in ('utf-8-sig', 'latin-1'):
        try:
            txt = raw.decode(enc)
        except UnicodeDecodeError:
            continue
        sep = ';' if txt.count(';') > txt.count(',') else ','
        return pd.read_csv(
            io.StringIO(txt), sep=sep, skiprows=skiprows, low_memory=False
        )
    raise ValueError(f"No se pudo decodificar {path} con utf-8 ni latin-1")


def descargar_csv(url: str, nombre: str, skiprows: int = 0,
                  timeout: int = 60) -> pd.DataFrame:
    """Descarga un CSV a data/raw si no existe y lo devuelve como DataFrame."""
    path = RAW_DIR / nombre
    if not path.exists():
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(r.content)
    return leer_csv_local(nombre, skiprows=skiprows)


def cargar_por_comuna(query: str, nombre: str, skiprows: int = 0) -> pd.DataFrame:
    """Carga el CSV local; solo consulta CKAN si aún no está descargado.

    Esto permite abrir la aplicación sin conexión, requisito para una
    demostración reproducible.
    """
    if (RAW_DIR / nombre).exists():
        return leer_csv_local(nombre, skiprows=skiprows)

    r = requests.get(CKAN_API, params={'q': query, 'rows': 1}, timeout=30)
    r.raise_for_status()
    d = r.json().get('result', {})
    if not d.get('count'):
        raise ValueError(f"No se encontró el conjunto: {query}")

    for res in d['results'][0].get('resources', []):
        if (res.get('format') or '').upper() == 'CSV':
            return descargar_csv(res['url'], nombre, skiprows=skiprows)
    raise ValueError(f"El conjunto no tiene recursos CSV: {query}")


def normalizar_comuna(val) -> str:
    """Normaliza cualquier variante a 'Comuna N' (N entre 1 y 22).

    La fuente mezcla 'Comuna 20', 'COMUNA 20' y '20'; sin esta
    normalización el cruce entre fuentes devuelve cero coincidencias.
    """
    if pd.isna(val):
        return "N/D"
    s = str(val).strip().upper()
    if s in ('N/D', 'N/A', '', 'NAN', 'NINGUNA', 'SIN DATO'):
        return "N/D"
    m = re.search(r'(\d{1,2})', s)
    if m:
        n = int(m.group(1))
        if 1 <= n <= 22:
            return f"Comuna {n}"
    return "N/D"


def normalizar_barrio(val) -> str:
    """Normaliza barrio a mayúsculas y sin espacios repetidos."""
    if pd.isna(val):
        return "N/D"
    s = re.sub(r'\s+', ' ', str(val).strip().upper())
    if s in ('N/D', 'N/A', '', 'NAN', 'NINGUNO'):
        return "N/D"
    return s


def parse_fecha_mes(val, anio_min: int = ANIO_MIN,
                    anio_max: int = ANIO_MAX):
    """Convierte 'dd/mm/aaaa' o 'ene-24' a 'aaaa-mm'.

    Devuelve None si la fecha no es válida o está fuera del rango
    documentado. Los formatos no reconocidos se descartan en lugar de
    inventar un período.
    """
    if pd.isna(val):
        return None

    s = str(val).strip()
    anio = mes = None

    if '/' in s:
        parts = s.split('/')
        if len(parts) == 3 and all(p.strip().isdigit() for p in parts):
            _, mes_txt, anio_txt = (p.strip() for p in parts)
            anio, mes = int(anio_txt), int(mes_txt)
    elif '-' in s:
        partes = s.split('-')
        if len(partes) == 2:
            nombres = {
                'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4, 'may': 5, 'jun': 6,
                'jul': 7, 'ago': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dic': 12,
            }
            clave = partes[0].strip().lower()[:3]
            if clave in nombres and partes[1].strip().isdigit():
                mes = nombres[clave]
                anio_txt = partes[1].strip()
                anio = int(anio_txt) if len(anio_txt) == 4 else 2000 + int(anio_txt)
    elif s.isdigit() and len(s) == 4:
        anio, mes = int(s), 1

    if anio is None or mes is None:
        return None
    if not (1 <= mes <= 12):
        return None
    if not (anio_min <= anio <= anio_max):
        return None
    return f"{anio:04d}-{mes:02d}"
