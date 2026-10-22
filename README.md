# CicloRoto

**Plataforma modular de trazabilidad de la gestión urbana de Cali, Colombia.**

CicloRoto analiza datos públicos para estudiar la relación entre los reportes ciudadanos y los registros de intervenciones urbanas. Su objetivo es identificar patrones territoriales y temporales, posibles brechas de trazabilidad y limitaciones en la información disponible.

## Problema

Los reportes ciudadanos y los registros de intervenciones públicas pueden encontrarse en conjuntos de datos diferentes. Cuando no existe un identificador común, resulta difícil verificar sistemáticamente cómo se relacionan ambas fuentes.

CicloRoto explora estas relaciones utilizando criterios territoriales y temporales, documentando la incertidumbre y los límites de cada comparación.

## Funcionalidades

- Descarga y procesamiento de datos públicos.
- Limpieza y normalización de registros.
- Comparación de reportes e intervenciones por territorio y período.
- Identificación de registros sin coincidencias en las fuentes consultadas.
- Visualización de resultados mediante Streamlit.
- Arquitectura modular para incorporar nuevas categorías de gestión urbana.

## Módulos

| Módulo | Estado | Funcionalidad |
|---|---|---|
| Alumbrado público | Implementado | Diagnostica si los reportes ciudadanos pueden vincularse a proyectos de alumbrado y mide la cobertura de ambas fuentes. |
| Malla vial | Planificado | Análisis de reportes e intervenciones de infraestructura vial. |

## Resultado del módulo activo

Con las fuentes públicas consultadas, **0 de 17,642 reportes pueden vincularse a una intervención de alumbrado**. No porque las obras no existan, sino porque las fuentes no lo permiten:

| Criterio | Estado |
|---|---|
| Clave territorial común | Parcial (normalizable a `Comuna 1`–`Comuna 22`) |
| Solapamiento temporal | **No** — PQR 2024-01 a 2025-11 frente a alumbrado de 2017 |
| Fecha por registro en alumbrado | **No** — el año solo aparece en el título del archivo |
| Categoría temática en PQR | **No** — no hay categoría de alumbrado |
| Identificador de caso | **No** — ninguna fuente lo publica |

Cifras verificadas (ver [`docs/audit.md`](docs/audit.md)):

| Métrica | Valor |
|---|---|
| PQR 2024–2025 | 17,642 (11,873 + 5,741) |
| Proyectos de alumbrado (2017) | 247 |
| Puntos luminosos | 3,686 |
| Inversión registrada | COP 1.862.820.659 |
| Comunas con proyecto | 12 de 22 |
| Reportes vinculables | 0 |

## Metodología y limitaciones

El módulo de alumbrado no fuerza un cruce que los datos no soportan: mide la brecha documental y describe la cobertura territorial de cada fuente.

- Las comunas se normalizan a `Comuna 1`–`Comuna 22` antes de cualquier comparación.
- Las fechas fuera de 2024–2025 se marcan como inválidas; no se imputan períodos.
- El período del alumbrado es el año del título del archivo (2017), no la columna `tipo`.
- `0 vinculables` significa "no verificable con estas fuentes", no "problema sin resolver".
- La comparación territorial entre 2024–2025 y 2017 es descriptiva, no causal.
- Los resultados dependen de las fuentes disponibles y de las reglas de normalización aplicadas.

## Arquitectura

```text
Fuentes públicas
      ↓
Descarga y limpieza
      ↓
Normalización de registros
      ↓
Motor de trazabilidad
      ↓
Módulos de análisis
      ↓
Panel interactivo en Streamlit
```

## Estructura del proyecto

```text
cicloroto/
├── core/          # Pipeline y motor de trazabilidad
├── modules/       # Módulos de análisis
├── data/
│   ├── raw/       # Datos originales descargados
│   └── processed/ # Datos transformados
├── app.py         # Interfaz Streamlit
├── tests/         # Pruebas automatizadas
├── requirements.txt
└── README.md
```

La estructura anterior es orientativa; consulta el repositorio para confirmar las rutas reales.

## Instalación

Requiere Python y las dependencias indicadas en `requirements.txt`.

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python -m streamlit run app.py
```

Los CSV están incluidos en `data/raw/`. La aplicación los lee del disco y **no necesita conexión a internet** para abrirse. Solo consulta CKAN si un archivo local falta.

## Pruebas

Ejecuta las pruebas automatizadas con el comando correspondiente a la configuración del proyecto. Si se utiliza `pytest`:

```bash
pytest -q
```

## Fuentes de datos

Catálogo normalizado: [`data/sources.csv`](data/sources.csv)

Registro de auditoría: [`docs/audit.md`](docs/audit.md)

Los conjuntos de datos se consultan en el portal de datos abiertos de Cali:

- [Portal de datos abiertos de Cali](https://datos.cali.gov.co/)

| ID | Nombre | Enlace directo | Período | Condiciones |
|---|---|---|---|---|
| S01 | Cantidad de PQR por comuna | [CKAN](https://datos.cali.gov.co/dataset/de6fa620-eda6-47c8-97ae-bcbbed493fe1) | 2024-2025 | CC-BY |
| S02 | Proyectos de alumbrado público | [CKAN](https://datos.cali.gov.co/dataset/e6a3fd08-6a44-422f-beb7-d21ac1f38ec1) | 2017 | CC-BY |
| S03 | Intersecciones semaforizadas | [CKAN](https://datos.cali.gov.co/dataset/daa6cec4-3fe2-4a5e-8194-91d30c7fcbb3) | 2025 | CC-BY | Complementaria |
| S04 | Recuperación malla vial | [CKAN](https://datos.cali.gov.co/dataset/a68cd30d-3be5-47b8-bb83-c6b85b86a5f6) | No especificado | CC-BY | Complementaria |
| S05 | Puntos de Ventanilla Única | [CKAN](https://datos.cali.gov.co/dataset/a2120ceb-af52-480f-bf7c-8cad6a333cba) | 2025 | CC-BY | Complementaria |

**Nota:** S03, S04 y S05 son fuentes complementarias. No se utilizan en el módulo activo (alumbrado).

## Licencias

- **Código:** MIT (ver [`LICENSE`](LICENSE)).
- **Datos:** CC-BY (Creative Commons Attribution). Atribución requerida: Alcaldía de Santiago de Cali / Secretaría correspondiente.

## Estado del proyecto

Prototipo en desarrollo. Los resultados deben interpretarse teniendo en cuenta la cobertura de los datos, los criterios de comparación y las limitaciones metodológicas documentadas.
