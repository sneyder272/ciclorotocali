# CicloRoto

Plataforma modular de trazabilidad de la gestión urbana de Cali, Colombia.

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

### Definición de "brecha de trazabilidad"

Una brecha de trazabilidad es un registro de reporte (PQR) para el cual **no se encontró intervención vinculada** en las fuentes consultadas, utilizando los criterios de comparación territorial y temporal definidos.

**Esto NO significa que el problema no haya sido resuelto.** Significa que, con los datos públicos disponibles y las reglas de comparación aplicadas, no fue posible vincular el reporte con una intervención.

## Arquitectura

```
Fuentes públicas (CKAN)
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

```
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

Requiere Python y las dependencias indicadas en requirements.txt.

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
streamlit run app.py
```

Ajusta el comando si el punto de entrada real de la aplicación es app.py en la raíz.

## Pruebas

Ejecuta las pruebas automatizadas con el comando correspondiente a la configuración del proyecto. Si se utiliza pytest:

```bash
pytest -q
```

## Reproducibilidad

### Fechas de consulta

| Fuente | Fecha de consulta | URL |
|---|---|---|
| PQR por comuna | 2026-10-19 | https://datos.cali.gov.co/dataset/de6fa620-eda6-47c8-97ae-bcbbed493fe1 |
| Alumbrado público | 2026-10-19 | https://datos.cali.gov.co/dataset/e6a3fd08-6a44-422f-beb7-d21ac1f38ec1 |
| Intersecciones semaforizadas | 2026-10-17 | https://datos.cali.gov.co/dataset/daa6cec4-3fe2-4a5e-8194-91d30c7fcbb3 |

### Pasos de limpieza

1. **PQR**: Normalización de comuna (string consistente), normalización de barrio (mayúsculas), parseo de fecha a período mes/año.
2. **Alumbrado**: Normalización de comuna y barrio, extracción de período del campo de tipo cuando es posible.
3. **Trazabilidad**: Agregación por comuna + período, cálculo de brechas, clasificación de nivel de trazabilidad.

## Fuentes de datos

Los conjuntos de datos se consultan en el portal de datos abiertos de Cali:

| Nombre | Enlace directo | Período | Condiciones |
|---|---|---|---|
| Cantidad de PQR por comuna | [CKAN](https://datos.cali.gov.co/dataset/de6fa620-eda6-47c8-97ae-bcbbed493fe1) | 2024 | CC-BY |
| Proyectos de alumbrado público | [CKAN](https://datos.cali.gov.co/dataset/e6a3fd08-6a44-422f-beb7-d21ac1f38ec1) | 2014-2019 | CC-BY |

## Licencias

- **Código**: Por definir (recomendado: MIT o Apache 2.0).
- **Datos**: Los datos públicos de Cali tienen licencia CC-BY. Consulte las condiciones específicas de cada fuente antes de reutilizar.

## Estado del proyecto

Prototipo en desarrollo. Los resultados deben interpretarse teniendo en cuenta la cobertura de los datos, los criterios de comparación y las limitaciones metodológicas documentadas.
