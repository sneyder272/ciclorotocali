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
| Alumbrado público | Implementado | Analiza la relación entre PQR e intervenciones registradas de alumbrado. |
| Malla vial | Planificado | Análisis de reportes e intervenciones de infraestructura vial. |

## Metodología y limitaciones

El módulo de alumbrado utiliza información territorial y temporal para explorar relaciones entre reportes e intervenciones.

- La comparación se realiza a nivel de comuna o barrio y período, según la disponibilidad de cada fuente.
- Una PQR sin coincidencia no demuestra que el problema continúe sin resolver.
- Una coincidencia territorial y temporal no demuestra causalidad ni confirma que una intervención haya resuelto un reporte específico.
- La cobertura, calidad y consistencia de los registros pueden variar entre años.
- Los resultados dependen de las fuentes disponibles y de las reglas de normalización y comparación aplicadas.

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
streamlit run cicloroto/app.py
```

Ajusta el comando si el punto de entrada real de la aplicación es `app.py` en la raíz.

## Pruebas

Ejecuta las pruebas automatizadas con el comando correspondiente a la configuración del proyecto. Si se utiliza `pytest`:

```bash
pytest -q
```

## Fuentes de datos

Los conjuntos de datos se consultan en el portal de datos abiertos de Cali:

- [Portal de datos abiertos de Cali](https://datos.cali.gov.co/)

Registra para cada conjunto de datos su nombre exacto, enlace directo, fecha de consulta, período cubierto y condiciones de uso.

## Licencias

La licencia del código y las condiciones de reutilización de los datos deben documentarse por separado, respetando los términos de cada fuente.

## Estado del proyecto

Prototipo en desarrollo. Los resultados deben interpretarse teniendo en cuenta la cobertura de los datos, los criterios de comparación y las limitaciones metodológicas documentadas.
