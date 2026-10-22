# Evidencia de fuentes y snapshots

**Captura:** 2026-10-22, 10:02 (America/Bogota).
**Portal:** `https://datos.cali.gov.co`.
**Estado:** suspendido temporalmente por seguridad.

## 1. Capturas del portal

Las tres URLs oficiales se abrieron en un navegador real (Edge headless,
ventana de 1440 × 1000) y devolvieron el mismo comunicado:

> **Suspensión temporal de servicios web por medidas de seguridad**
> Cali, 21 de octubre de 2026

| Archivo | URL consultada | Qué muestra |
|---|---|---|
| [`v01_lesionados.png`](v01_lesionados.png) | https://datos.cali.gov.co/dataset/75c089ba-7df3-4816-b80f-c69c6e5362ae | Comunicado de suspensión del portal |
| [`a01_alumbrado.png`](a01_alumbrado.png) | https://datos.cali.gov.co/dataset/e6a3fd08-6a44-422f-beb7-d21ac1f38ec1 | El mismo comunicado |
| [`a02_pqr.png`](a02_pqr.png) | https://datos.cali.gov.co/dataset/de6fa620-eda6-47c8-97ae-bcbbed493fe1 | El mismo comunicado |

Las capturas documentan el estado del portal el **22 de octubre de 2026**, no
la ficha de metadatos de cada conjunto. Los CSV se descargaron antes de la
suspensión (17 y 19 de octubre) y se incluyen en el repositorio para que el
análisis siga siendo reproducible.

## 1.1 Captura de la app

| Archivo | Fecha | Qué muestra |
|---|---|---|
| [`app_home.png`](app_home.png) | 2026-10-22 | Vista real de `http://localhost:8501`: KPIs, aviso del cruce crítico y las cuatro pestañas |

No es una captura de una fuente oficial; es evidencia de que la app renderiza
con los CSV locales. La demostración en video debe grabarse en vivo.

## 2. Snapshots usados

Los archivos de `data/raw/` son los insumos exactos del producto. Sus hashes
están en [`checksums.sha256`](checksums.sha256).

| ID | Conjunto | Filas de datos | Filas usadas | Período | Licencia | Consulta | SHA-256 |
|---|---|---:|---:|---|---|---|---|
| V01 | Lesionados en accidentes de tránsito | 51,236 | 51,236 | 2016–2025 | CC-BY | 2026-10-17 | `0fc3ec41…cfee989` |
| A01 | Proyectos de alumbrado público | 251 | 247 | 2017 | CC-BY | 2026-10-19 | `4c4e20df…9201358` |
| A02 | PQR por comuna | 17,642 | 17,642 | 2024–2025 | CC-BY | 2026-10-19 | `df8f4204…f0f5c8f` |

Hashes completos:

```text
0fc3ec413459624a0ac03efccc7b8062b99cf2af307e3a9e123976127cfee989  data/raw/lesionados_2016_2025.csv
4c4e20df70d02693671698bba72402e403f7f81d7dcb1c32893f899849201358  data/raw/alumbrado_publico.csv
df8f42048b09030f1a8a5fb9a63adbacae06d53b0ed18e6629a07609ff0f5c8f  data/raw/pqrs_por_comuna.csv
```

### Columnas procesadas

- **V01:** `fecha`, `hora`, `tipo`, `placa`, `direccion`, `mecanismo`,
  `automovil`, `moto`, `ciclista`, `peaton`, `hora_num`, `anio`, `cruce`.
- **A01:** `item`, `proyecto`, `direccion`, `barrio`, `tipo`,
  `valor_aprobado`, `puntos_luminosos`, `comuna`, `proyectos`,
  `proyectos_especiales`, `periodo`.
- **A02:** `fecha_reporte`, `clase_peticion`, `comuna`, `barrio`, `periodo`,
  `anio`.

## 3. Verificar la integridad

Desde la raíz del repositorio:

```bash
python scripts/verificar_checksums.py
```

Salida esperada:

```text
OK  data/raw/lesionados_2016_2025.csv
OK  data/raw/alumbrado_publico.csv
OK  data/raw/pqrs_por_comuna.csv
3 archivos verificados.
```

En Linux/macOS también funciona:

```bash
sha256sum -c docs/evidence/checksums.sha256
```

En Windows PowerShell:

```powershell
Get-FileHash data/raw/lesionados_2016_2025.csv -Algorithm SHA256
```

## 4. Por qué no hay datos nuevos

La consulta del 22 de octubre devolvió el comunicado de suspensión. No se
descargaron ni se inventaron datos después del 19 de octubre. Cualquier
actualización del portal requeriría una nueva consulta y un nuevo snapshot; no
se presenta como si ya existiera.

## 5. Licencias

- **Datos:** CC-BY, Alcaldía de Santiago de Cali / dependencia responsable.
- **Código:** MIT (`LICENSE`).
- La licencia de los datos no cubre el código ni viceversa.
