"""CicloRoto: módulo de siniestralidad vial.

Fuente: Secretaría de Movilidad de Cali, "Lesionados en accidentes de
tránsito" (2016-2025), 51,236 registros con dirección textual.

Qué hace
--------
1. Normaliza direcciones y consolida variantes del mismo cruce
   ('CRA 8 CON CL 70' y 'CALLE 70 CON CARRERA 8' son la misma esquina).
2. Rankea cruces por tasa ajustada con un modelo jerárquico Gamma-Poisson
   (empirical Bayes), reportando intervalo de confianza.
3. Describe patrón horario, tipo de víctima y mecanismo.

Límites
-------
- Solo 42.1% de los registros tienen una dirección resoluble a cruce.
- No hay coordenadas ni volumen de tráfico: no se corrige por exposición.
- 2025 está incompleto.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.pipeline import leer_csv_local

COLUMNAS = [
    'fecha', 'hora', 'tipo', 'placa', 'direccion', 'mecanismo',
    'automovil', 'moto', 'ciclista', 'peaton',
]

VIA_RE = r'^(CALLE|CARRERA|AVENIDA|DIAGONAL|TRANSVERSAL)'
VIA_TOKEN = (
    r'(?:CALLE|CARRERA|AVENIDA|DIAGONAL|TRANSVERSAL)\s+'
    r'[0-9]+(?:\s*[A-Z](?![A-Z]))?(?:\s+(?:BIS|NORTE|SUR|ESTE|OESTE))?'
)
ABREVIATURAS = {
    r'\bCRA\b': 'CARRERA', r'\bCARR\b': 'CARRERA', r'\bKR\b': 'CARRERA',
    r'\bCL\b': 'CALLE', r'\bCLL\b': 'CALLE',
    r'\bAV\b': 'AVENIDA', r'\bAVDA\b': 'AVENIDA',
    r'\bTRANS\b': 'TRANSVERSAL', r'\bTV\b': 'TRANSVERSAL',
    r'\bDIAG\b': 'DIAGONAL', r'\bDG\b': 'DIAGONAL',
}

MECANISMOS = {
    'CHOQUE CON LESIONADOS': 'Choque con lesionados',
    'CON HERIDOS': 'Choque con lesionados',
    'POR ATROPELLO': 'Atropello',
    'POR VOLCAMIENTO': 'Volcamiento',
    'POR CAIDA DE OCUPANTE': 'Caída de ocupante',
}


def normalizar_direccion(valor) -> str:
    """Mayúsculas, sin puntuación final y con abreviaturas expandidas."""
    s = str(valor).strip().upper()
    s = re.sub(r'[.,;]+$', '', s)
    for patron, reemplazo in ABREVIATURAS.items():
        s = re.sub(patron, reemplazo, s)
    return re.sub(r'\s+', ' ', s)


def canonicalizar_cruce(valor):
    """Devuelve 'VIA A CON VIA B' ordenado, o None si no es un cruce.

    El orden alfabético hace que 'CARRERA 8 CON CALLE 70' y
    'CALLE 70 CON CARRERA 8' cuenten como la misma esquina.
    """
    s = normalizar_direccion(valor)
    # Unifica 'CALLE 8 A' con 'CALLE 8A'
    s = re.sub(r'([0-9])\s+([A-Z])\b', r'\1\2', s)

    for separador in (' CON ', ' Y ', ' ESQUINA ', '/', '&'):
        s = s.replace(separador, '|')

    partes = [p.strip() for p in s.split('|') if p.strip()]
    partes = [p for p in partes if re.match(VIA_RE, p)]

    if len(partes) < 2:
        # Formatos sin conector: 'CALLE 25 CARRERA 109'
        partes = re.findall(VIA_TOKEN, s)

    if len(partes) < 2:
        return None

    limpias = []
    for p in partes[:2]:
        p = re.sub(r'\s+', ' ', p.strip())
        limpias.append(p)
    return ' CON '.join(sorted(limpias))


def _mecanismo(valor) -> str:
    s = str(valor).strip().upper()
    return MECANISMOS.get(s, 'Sin dato / otro')


def _ventana_pico(horas: pd.Series):
    """Devuelve la ventana de 3 horas con más siniestros.

    Un solo modo horario es inestable cuando hay empates; la ventana de
    3 horas resume mejor el patrón.
    """
    horas = horas.dropna()
    if horas.empty:
        return None
    conteo = horas.value_counts().reindex(range(24), fill_value=0)
    ventanas = {
        h: conteo[[h, (h + 1) % 24, (h + 2) % 24]].sum() for h in range(24)
    }
    inicio = max(ventanas, key=ventanas.get)
    return f'{inicio:02d}:00–{(inicio + 2) % 24:02d}:59'


def cargar_datos() -> pd.DataFrame:
    """Carga, limpia y enriquece los registros de lesionados."""
    df = leer_csv_local('lesionados_2016_2025.csv')
    if len(df.columns) != len(COLUMNAS):
        raise ValueError(
            f'Se esperaban {len(COLUMNAS)} columnas y llegaron {len(df.columns)}'
        )
    df.columns = COLUMNAS

    df['fecha'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y', errors='coerce')
    df['hora_num'] = pd.to_datetime(
        df['hora'].astype(str).str.strip(), format='%H:%M', errors='coerce'
    ).dt.hour
    df['anio'] = df['fecha'].dt.year

    df['mecanismo'] = df['mecanismo'].apply(_mecanismo)
    df['cruce'] = df['direccion'].apply(canonicalizar_cruce)

    for col in ['automovil', 'moto', 'ciclista', 'peaton']:
        df[col] = df[col].astype(str).str.strip().eq('1')

    return df


def _parametros_empiricos(conteos: pd.Series) -> tuple[float, float]:
    """Estima la previa Gamma(alpha, beta) por momentos.

    Si no hay sobredispersión, usa una previa débil (poca contracción).
    """
    mu = float(conteos.mean())
    var = float(conteos.var(ddof=1))
    if not np.isfinite(var) or var <= mu or mu <= 0:
        alpha = 1000.0
        beta = alpha / max(mu, 1e-6)
        return alpha, beta
    alpha = mu ** 2 / (var - mu)
    beta = mu / (var - mu)
    return alpha, beta


def _ranking(validos: pd.DataFrame, min_registros: int) -> pd.DataFrame:
    """Agrega por cruce y calcula la tasa ajustada con su intervalo."""
    if validos.empty:
        return pd.DataFrame()

    # Filtrar antes de calcular ventanas: con el mínimo de 1 hay miles de
    # cruces y un apply por grupo tarda minutos.
    conteos = validos['cruce'].value_counts()
    elegibles = conteos[conteos >= min_registros].index
    v = validos[validos['cruce'].isin(elegibles)]
    if v.empty:
        return pd.DataFrame()

    ranking = v.groupby('cruce').agg(
        registros=('cruce', 'size'),
        pct_moto=('moto', 'mean'),
        pct_peaton=('peaton', 'mean'),
        pct_ciclista=('ciclista', 'mean'),
        anios_con_registro=('anio', 'nunique'),
    ).reset_index()

    # Ventana pico de 3 horas, vectorizada para todos los cruces a la vez.
    con_hora = v.dropna(subset=['hora_num'])
    if con_hora.empty:
        ranking['ventana_pico'] = None
    else:
        matriz = pd.crosstab(
            con_hora['cruce'], con_hora['hora_num'].astype(int)
        ).reindex(
            index=ranking['cruce'].tolist(), columns=range(24), fill_value=0
        )
        valores = matriz.to_numpy()
        sumas = np.stack([
            valores[:, [h, (h + 1) % 24, (h + 2) % 24]].sum(axis=1)
            for h in range(24)
        ], axis=1)
        inicio = sumas.argmax(axis=1)
        etiquetas = np.array(
            [f'{h:02d}:00–{(h + 2) % 24:02d}:59' for h in inicio],
            dtype=object,
        )
        etiquetas[valores.sum(axis=1) == 0] = None
        ranking['ventana_pico'] = etiquetas

    alpha, beta = _parametros_empiricos(ranking['registros'])
    ranking['tasa_ajustada'] = (alpha + ranking['registros']) / (beta + 1)
    error = np.sqrt(ranking['tasa_ajustada'] / (beta + 1))
    ranking['ic_inferior'] = (ranking['tasa_ajustada'] - 1.96 * error).clip(lower=0)
    ranking['ic_superior'] = ranking['tasa_ajustada'] + 1.96 * error
    ranking['veces_promedio'] = ranking['tasa_ajustada'] / max(ranking['registros'].mean(), 1e-9)

    ranking = ranking.sort_values(
        ['tasa_ajustada', 'registros'], ascending=False
    ).reset_index(drop=True)
    ranking.insert(0, 'puesto', ranking.index + 1)

    for col in ['pct_moto', 'pct_peaton', 'pct_ciclista']:
        ranking[col] = (100 * ranking[col]).round(1)
    for col in ['tasa_ajustada', 'ic_inferior', 'ic_superior', 'veces_promedio']:
        ranking[col] = ranking[col].round(1)

    return ranking


def generar_ficha(detalle: pd.DataFrame, cruce: str) -> str:
    """Genera una ficha imprimible y una solicitud lista para radicar.

    El texto no afirma que falte una obra: pide la información que permitiría
    verificarlo. Es el paso que convierte el hallazgo en una acción ciudadana.
    """
    n = len(detalle)
    anios = sorted(int(a) for a in detalle['anio'].dropna().unique())
    rango = f'{anios[0]}–{anios[-1]}' if anios else 'sin fecha'
    moto = 100 * detalle['moto'].mean()
    peaton = 100 * detalle['peaton'].mean()
    ventana = _ventana_pico(detalle['hora_num']) or 'sin dato'

    mecanismos = detalle['mecanismo'].value_counts()
    lista_mec = ', '.join(
        f'{m} ({c})' for m, c in mecanismos.head(3).items()
    )
    nombre = cruce.title().replace(' Con ', ' con ')

    return f"""# Ficha de seguridad vial

## {nombre}

**{n} siniestros con lesionados** registrados entre {rango}.
Es un conteo de siniestros, no de personas.

| Indicador | Valor |
|---|---|
| Motocicleta | {moto:.0f}% de los registros |
| Peatón | {peaton:.0f}% de los registros |
| Ventana horaria con más casos | {ventana} |
| Mecanismos más frecuentes | {lista_mec} |
| Años con dirección utilizable | {', '.join(str(a) for a in anios)} |

### Lo que esta ficha no puede afirmar

La Secretaría de Movilidad publica la dirección de los siniestros, pero los
conjuntos de obras consultados no permiten vincular una intervención con este
cruce y una fecha. Por eso **no se afirma que falte una obra** ni que el
problema siga sin resolver: se afirma que no es verificable con lo publicado.

### Solicitud lista para radicar

> **Solicitud de información — seguridad vial en {nombre}**
>
> Cordial saludo,
>
> En ejercicio del derecho de petición (Ley 1755 de 2015), solicito
> información pública sobre las intervenciones de infraestructura y
> señalización realizadas en el cruce **{nombre}** entre {rango}:
>
> 1. Si se ejecutaron obras de señalización, iluminación o rediseño
>    geométrico en ese cruce.
> 2. La fecha, el identificador y el estado de cada intervención.
> 3. Si existe un estudio de siniestralidad o una auditoría de seguridad
>    vial para ese punto.
>
> Fundamento de la solicitud: la fuente pública de lesionados registra
> {n} siniestros con lesionados en ese cruce entre {rango}. Los conjuntos
> de obras consultados no permiten vincular una intervención con ese cruce
> y esa fecha.
>
> Atentamente,
>
> [Nombre completo]
> [Cédula]
> [Correo electrónico]

**Dónde radicar:** Ventanilla Única de la Alcaldía de Cali o el canal
virtual de la Secretaría de Movilidad.

*Fuente: datos.cali.gov.co, Secretaría de Movilidad, consulta 2026-10-17.
Licencia CC-BY. Generado por CicloRoto Vial.*
"""


def generar_panel(df: pd.DataFrame, min_registros: int = 5,
                  anio=None, mecanismo=None) -> dict:
    """Genera ranking, series temporales y KPIs."""
    d = df
    if anio is not None:
        d = d[d['anio'] == anio]
    if mecanismo and mecanismo != 'Todos':
        d = d[d['mecanismo'] == mecanismo]

    validos = d[d['cruce'].notna()]
    ranking = _ranking(validos, min_registros)

    por_anio = (
        d.dropna(subset=['anio']).groupby('anio').size().rename('registros')
    )
    por_hora = (
        d.dropna(subset=['hora_num']).groupby('hora_num').size()
        .reindex(range(24), fill_value=0).rename('registros')
    )
    por_mecanismo = d['mecanismo'].value_counts().rename('registros')
    por_victima = pd.Series({
        'Motocicleta': int(d['moto'].sum()),
        'Automóvil': int(d['automovil'].sum()),
        'Peatón': int(d['peaton'].sum()),
        'Ciclista': int(d['ciclista'].sum()),
    })

    total = len(d)
    con_cruce = int(d['cruce'].notna().sum())
    top = ranking.iloc[0] if not ranking.empty else None

    kpis = {
        'total_registros': total,
        'con_cruce': con_cruce,
        'pct_con_cruce': round(100 * con_cruce / total, 1) if total else 0.0,
        'cruces_distintos': int(validos['cruce'].nunique()),
        'pct_moto': round(100 * d['moto'].mean(), 1) if total else 0.0,
        'pct_peaton': round(100 * d['peaton'].mean(), 1) if total else 0.0,
        'top_cruce': top['cruce'] if top is not None else 'Sin datos',
        'top_registros': int(top['registros']) if top is not None else 0,
        'anio_min': int(d['anio'].min()) if d['anio'].notna().any() else None,
        'anio_max': int(d['anio'].max()) if d['anio'].notna().any() else None,
    }

    return {
        'kpis': kpis,
        'ranking': ranking,
        'por_anio': por_anio,
        'por_hora': por_hora,
        'por_mecanismo': por_mecanismo,
        'por_victima': por_victima,
        'total_filtrado': total,
    }


if __name__ == '__main__':
    datos = cargar_datos()
    panel = generar_panel(datos)
    print(f"Registros: {panel['kpis']['total_registros']:,}")
    print(f"Con cruce: {panel['kpis']['con_cruce']:,} "
          f"({panel['kpis']['pct_con_cruce']}%)")
    print(f"Cruces distintos: {panel['kpis']['cruces_distintos']:,}")
    print()
    print(panel['ranking'].head(10).to_string(index=False))
