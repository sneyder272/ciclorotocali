# Registro de auditoría de datos — CicloRoto

**Fecha de consulta:** 2026-10-19
**Módulo:** Alumbrado público

## 1. Descarga

| Fuente | Líneas del archivo | Filas de datos | Nota |
|---|---|---|---|
| S01: PQR por comuna | 17,643 | **17,642** | Una línea de encabezado. |
| S02: Proyectos de alumbrado | 253 | **251** | Una línea de título (`... AÑO 2017`) y una de encabezado. |

## 2. Procesamiento

| Fuente | Filas de datos | Filas usadas | Descartadas | Causa |
|---|---|---|---|---|
| S01: PQR | 17,642 | 17,642 | 0 | Se conservan todas; las fechas inválidas se marcan, no se borran. |
| S02: Alumbrado | 251 | 247 | 4 | Sin comuna válida (1–22). |

### Detalle de las 4 filas descartadas (S02)

| Métrica | Valor |
|---|---|
| Puntos luminosos no contabilizados | 39 |
| Inversión no contabilizada (COP) | 55.907.038 |

Las filas se descartan del análisis territorial porque no es posible
asignarlas a una comuna. No se imputan valores.

### Fechas inválidas en S01

| Situación | Registros |
|---|---|
| Sin fecha | 17 |
| Año fuera de 2024–2025 (2005, 2026, 2027, 2028, 2205) | 11 |
| **Total sin período válido** | **28** |

Estos 28 registros permanecen en el conteo total (17,642) pero no entran en
los agregados por período.

### Comunas sin dato en S01

| Situación | Registros | Porcentaje |
|---|---|---|
| Comuna `N/D` | 2,673 | 15.1% |

Las variantes `Comuna 20`, `COMUNA 20` y `20` se normalizan a `Comuna 20`.
Sin esa normalización la fuente reporta 83 valores distintos; tras normalizar
quedan 22 comunas y `N/D`.

## 3. Cifras verificadas

| Métrica | Valor |
|---|---|
| PQR totales | 17,642 |
| PQR de 2024 | 11,873 |
| PQR de 2025 | 5,741 |
| Proyectos de alumbrado (2017) | 247 |
| Puntos luminosos registrados | 3,686 |
| Inversión registrada (COP) | 1.862.820.659 |
| Comunas con proyecto en 2017 | 12 de 22 |
| Reportes vinculables a una obra | **0** |

## 4. Por qué el cruce no es posible

| Criterio | Estado | Detalle |
|---|---|---|
| Clave territorial común | Parcial | Normalizable a `Comuna 1`–`Comuna 22`; no hay clave de caso. |
| Solapamiento temporal | **No** | PQR 2024-01 a 2025-11; alumbrado 2017. Meses en común: 0. |
| Fecha por registro en alumbrado | **No** | El año solo aparece en el título del archivo. |
| Categoría temática en PQR | **No** | Las clases son `Pqr`, `Cita médica`, `Denuncia`, `Urgencias`, etc. Ninguna identifica alumbrado. |
| Identificador de caso | **No** | Ninguna fuente publica un número de caso. |

**Conclusión:** `0 reportes vinculables` significa que la vinculación **no es
verificable con las fuentes públicas consultadas**. No significa que las obras
no existan ni que los reportes no hayan sido atendidos.

## 5. Corrección respecto a versiones anteriores

La primera versión del módulo calculaba el período del alumbrado a partir de
la columna `tipo` (valores `VIAS`, `CPL`, `ZONA VERDE`, etc.). Esa columna no
contiene fechas: todas las filas quedaban sin período y el agrupamiento las
descartaba, produciendo cifras de "brecha" que eran un artefacto del código.
También se afirmaba que el alumbrado cubría 2014–2019; el archivo corresponde
a **2017**, según su título.

Las cifras de esta versión reemplazan a las anteriores (748 brechas y 17,625
reportes sin intervención), que no deben usarse.

## 6. Fuentes complementarias (no usadas en el módulo activo)

| Fuente | Estado |
|---|---|
| S03: Intersecciones semaforizadas | Planificada (movilidad) |
| S04: Recuperación malla vial | Planificada (infraestructura vial) |
| S05: Puntos de Ventanilla Única | Referencia de acceso ciudadano |

## 7. Licencias

- Los conjuntos se publican como **CC-BY** en el catálogo de datos abiertos.
- Atribución: Alcaldía de Santiago de Cali / dependencia responsable.
- La licencia del código se documenta por separado en `LICENSE`.
