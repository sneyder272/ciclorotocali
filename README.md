# CicloRoto

Plataforma modular de trazabilidad de gestión urbana para Cali.

## Qué hace

Conecta reportes ciudadanos (PQR) con intervenciones públicas (alumbrado, malla vial, etc.) para identificar brechas en el ciclo de gestión urbana.

## Módulos disponibles

| Módulo | Estado | Descripción |
|---|---|---|
| **Alumbrado** | ✅ Activo | Conecta PQR con proyectos de alumbrado público |

## Cómo agregar un módulo nuevo

1. Crear `cicloroto/modules/<nombre_modulo>.py`
2. Implementar `cargar_datos()` y `generar_panel(pqr, intervenciones)`
3. Importar en `cicloroto/app.py`

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
streamlit run cicloroto/app.py
```

## Estructura

```
cicloroto/
  core/           # Pipeline y motor de trazabilidad
  modules/       # Módulos plug-and-play
  data/
    raw/          # Datos descargados
    processed/    # Datos procesados
  app.py          # Interfaz web
  tests/          # Tests automatizados
```

## Fuentes

- datos.cali.gov.co (CKAN): PQR, Alumbrado, Malla vial
- Licencia: CC-BY

## Limitaciones

- Conexión a nivel Comuna/Barrio + período (mes/año)
- NO se puede afirmar que una intervención específica resolvió un reporte específico
- Los datos de alumbrado tienen formatos inconsistentes entre años
