# Auditoría de datos — CicloRoto Vial

**Consulta:** 2026-10-17 (V01) y 2026-10-19 (A01, A02)
**Fuente principal:** Secretaría de Movilidad de Cali, conjunto V01.

## 1. Módulo vial (producto principal)

### 1.1 Descarga y volumen

| Concepto | Valor |
|---|---:|
| Filas del archivo | 51,236 |
| Columnas | 10 |
| Encoding | latin-1 |
| Separador | `;` |
| Rango de fechas | 2016-01-01 a 2025-12-09 |
| Filas sin fecha válida | 166 (0.3%) |

Las 166 filas sin fecha se conservan en el total, pero no entran en las series
por año.

### 1.2 Direcciones

| Concepto | Valor |
|---|---:|
| Registros con dirección resoluble a cruce | **28,411** |
| Porcentaje | **55.5%** |
| Cruces distintos | **9,261** |
| Cruces con 5 o más registros | **1,228** |

Cobertura por año:

| Año | Registros | Con cruce | Cobertura |
|---|---:|---:|---:|
| 2016 | 8,215 | 7,568 | 92.1% |
| 2017 | 6,985 | 4,429 | 63.4% |
| 2018 | 6,475 | 0 | **0.0%** |
| 2019 | 5,974 | 0 | **0.0%** |
| 2020 | 4,167 | 0 | **0.0%** |
| 2021 | 4,175 | 2,624 | 62.9% |
| 2022 | 4,131 | 3,721 | 90.1% |
| 2023 | 3,963 | 3,573 | 90.2% |
| 2024 | 4,126 | 3,845 | 93.2% |
| 2025 | 2,859 | 2,499 | 87.4% |

**Hallazgo:** 2018, 2019 y 2020 tienen la dirección vacía (`"."`) en el 100% de
los registros. Son 16,616 filas que no pueden ubicarse en un cruce. El ranking
se apoya en 2016, 2017 y 2021–2025, y así se declara en la aplicación.

### 1.3 Normalización aplicada

- Mayúsculas y eliminación de puntuación final.
- Abreviaturas: `CRA`/`CARR`/`KR` → `CARRERA`; `CL`/`CLL` → `CALLE`;
  `AV`/`AVDA` → `AVENIDA`; `TRANS`/`TV` → `TRANSVERSAL`;
  `DIAG`/`DG` → `DIAGONAL`.
- Separadores: `CON`, `Y`, `&`, `/`, `ESQUINA` y formato sin conector
  (`CALLE 25 CARRERA 109`).
- Se ordenan las dos vías alfabéticamente, de modo que
  `CARRERA 8 CON CALLE 70` y `CALLE 70 CON CARRERA 8` cuentan como el mismo
  cruce.
- Se descartan direcciones que no contienen dos vías (clínicas, CAI, `"."`).

### 1.4 Top 5 de cruces

| # | Cruce | Registros | % moto | % peatón | Ventana pico |
|---:|---|---:|---:|---:|---|
| 1 | Calle 70 con Carrera 8 | 148 | 41.2% | 12.8% | 16:00–18:59 |
| 2 | Carrera 23 con Transversal 25 | 125 | 46.4% | 3.2% | 08:00–10:59 |
| 3 | Calle 70 con Carrera 1 | 118 | 39.8% | 3.4% | 13:00–15:59 |
| 4 | Calle 34 con Carrera 1 | 107 | 45.8% | 5.6% | 14:00–16:59 |
| 5 | Calle 70 con Carrera 28D | 99 | 45.5% | 2.0% | 16:00–18:59 |

### 1.5 Modelo

- **Gamma-Poisson (empirical Bayes).** La previa se estima por momentos sobre
  los conteos de los cruces con al menos 5 registros.
- La media posterior es `(α + y) / (β + 1)`; el intervalo del 95% se aproxima
  con la desviación de la posterior.
- **No corrige por exposición** (volumen de tráfico), porque no está publicado.
  El ranking ordena por conteo ajustado; el intervalo comunica la incertidumbre.
- Un registro es un siniestro, no una persona. Los flags de víctima pueden
  faltar, así que los porcentajes son sobre registros, no sobre víctimas únicas.

### 1.6 Ficha y solicitud

La ficha por cruce se genera con los datos del propio cruce y una solicitud de
información basada en la Ley 1755 de 2015. **No afirma que falte una obra**:
pide la información que permitiría verificarlo.

## 2. Módulo de alumbrado (capa de trazabilidad)

### 2.1 Volumen

| Fuente | Líneas | Filas de datos | Usadas | Descartadas |
|---|---:|---:|---:|---:|
| A01 Alumbrado | 253 | 251 | 247 | 4 sin comuna válida |
| A02 PQR | 17,643 | 17,642 | 17,642 | 0 |

### 2.2 Por qué no se puede vincular

| Criterio | Estado | Detalle |
|---|---|---|
| Clave territorial común | Parcial | Normalizable a `Comuna 1`–`Comuna 22`; no hay clave de caso |
| Solapamiento temporal | **No** | PQR 2024-01 a 2025-11; alumbrado 2017 |
| Fecha por registro en alumbrado | **No** | El año solo figura en el título del archivo |
| Categoría temática en PQR | **No** | `Pqr`, `Cita médica`, `Denuncia`, etc. |
| Identificador de caso | **No** | Ninguna fuente lo publica |

**Conclusión:** `0 reportes vinculables` significa "no verificable con estas
fuentes", no "problema sin resolver".

### 2.3 Corrección de una versión anterior

La primera versión calculaba el período del alumbrado desde la columna `tipo`
(`VIAS`, `CPL`, `ZONA VERDE`). Esa columna no contiene fechas: todas las filas
quedaban sin período, el agrupamiento las descartaba y producía cifras de
"brecha" que eran un artefacto. También se afirmaba que el alumbrado cubría
2014–2019; el archivo corresponde a **2017**.

Las cifras de esta versión reemplazan a las anteriores (748 brechas y 17,625
reportes sin intervención), que no deben usarse.

## 3. Licencias

- Datos: **CC-BY**, Alcaldía de Santiago de Cali / dependencia responsable.
- Código: **MIT** (ver `LICENSE`).
- La licencia de los datos no cubre el código ni viceversa.

## 4. Estado del portal y snapshots

El **2026-10-22** las tres URLs de datos.cali.gov.co devolvieron un comunicado
oficial de **suspensión temporal de servicios web por medidas de seguridad**
(fechado 2026-10-21). No se descargaron datos nuevos después del 2026-10-19.

Los CSV usados se descargaron el 2026-10-17 (V01) y el 2026-10-19 (A01, A02),
antes de la suspensión. Están incluidos en data/raw/ con SHA-256 en
docs/evidence/checksums.sha256; las capturas y el detalle están en
docs/evidence/sources.md.

