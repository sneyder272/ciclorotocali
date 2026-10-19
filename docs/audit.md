# Registro de Auditoría de Datos — CicloRoto

**Fecha:** 2026-10-19

## Módulo: Alumbrado

### Descarga

| Fuente | Registros publicados | Registros descargados | Diferencia |
|---|---|---|---|
| S01: PQR por comuna | 17,642 | 17,642 | 0 |
| S02: Alumbrado público | 253 | 253 | 0 |

### Procesamiento

| Fuente | Registros descargados | Registros procesados | Diferencia | Causa |
|---|---|---|---|---|
| S01: PQR por comuna | 17,642 | 17,642 | 0 | Todos válidos |
| S02: Alumbrado público | 253 | 248 | 5 | Filas con datos faltantes en campos clave (comuna/barrio/tipo) |

### Causas de descarte (S02: Alumbrado)

| Causa | Registros |
|---|---|
| Comuna vacía o inválida | 3 |
| Barrio vacío | 1 |
| Tipo de proyecto no identificable | 1 |
| **Total descartados** | **5** |

## Justificación temporal

- **S01 (PQR):** 2024 (enero-diciembre)
- **S02 (Alumbrado):** 2014-2019 (agregado por mes/año)

**Nota:** La comparación entre PQR (2024) e intervenciones de alumbrado (2014-2019) tiene una **desalineación temporal**. La trazabilidad calculada identifica coincidencias territoriales y temporales, pero la diferencia de períodos limita la interpretación causal. Los resultados deben leerse como "ausencia de intervención vinculada en las fuentes consultadas", no como "problema sin resolver".

## Fuentes complementarias (no usadas en módulo activo)

| Fuente | Motivo de conservación |
|---|---|
| S03: Intersecciones semaforizadas | Módulo planificado (movilidad) |
| S04: Recuperación malla vial | Módulo planificado (infraestructura vial) |
| S05: Ventanilla Única | Referencia de acceso ciudadano |

## Licencias

- Todos los datasets: **CC-BY** (Creative Commons Attribution)
- Requisito: Atribuir la fuente original (Alcaldía de Santiago de Cali / Secretaría correspondiente)
