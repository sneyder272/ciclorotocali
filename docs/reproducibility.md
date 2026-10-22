# Reproducibilidad

**Objetivo:** que un jurado pueda clonar el repositorio, instalar dependencias,
verificar los datos y abrir la app sin pasos ocultos.

## Entorno probado

- Windows 11, PowerShell 5.1.
- Python **3.14.7** en la verificación local.
- El workflow de CI apunta a Python **3.12**.
- La app requiere Python **3.10 o superior**.

## 1. Clonar e instalar

```bash
git clone https://github.com/sneyder272/ciclorotocali.git
cd ciclorotocali
python -m venv .venv
```

Activar el entorno:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# Linux / macOS
source .venv/bin/activate
```

Instalar dependencias de ejecución y de prueba:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
```

## 2. Verificar los datos

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

Los CSV están normalizados a LF con `.gitattributes`, de modo que los SHA-256
no cambian entre Windows, Linux y macOS. Si un hash falla, el archivo fue
modificado: no continúes con el análisis.

## 3. Ejecutar las pruebas

```bash
pytest -q
```

Salida esperada:

```text
................                                                         [100%]
16 passed in ~15s
```

Las pruebas cubren conteos exactos, normalización de direcciones, filtros,
ficha, trazabilidad y el render de la app. Si falla una, revisa primero que
estés en la raíz del repositorio y que los CSV no hayan cambiado.

## 4. Abrir la app

```bash
python -m streamlit run app.py
```

Abre `http://localhost:8501`. La app no necesita internet: lee los CSV locales
de `data/raw/`.

Comprobación rápida del servicio:

```bash
curl http://localhost:8501/_stcore/health
# ok
```

En PowerShell:

```powershell
(Invoke-WebRequest -UseBasicParsing http://localhost:8501/_stcore/health).Content
# ok
```

## 5. Demo mínima

1. Abre la pestaña **Buscar mi esquina**.
2. Escribe `CL 70 & CRA 8`.
3. Verifica **148** registros y la fila `CALLE 70 CON CARRERA 8`.
4. Abre **Ficha y solicitud lista para radicar**.
5. Revisa **Trazabilidad**: `0 de 17,642` reportes vinculables.

## 6. Comprobar el estado del portal

El **2026-10-22** las URLs de `datos.cali.gov.co` devolvieron un comunicado de
suspensión temporal por seguridad (fechado 2026-10-21). Por eso los enlaces
oficiales pueden no abrir la ficha del conjunto. Los CSV usados están en el
repositorio y sus hashes están en `docs/evidence/checksums.sha256`. Capturas:
`docs/evidence/sources.md`.

## 7. CI

El workflow [`.github/workflows/tests.yml`](../.github/workflows/tests.yml)
instala las dependencias y ejecuta `pytest -q` en cada push. Si una ejecución
queda en `queued`, es un problema de la cola de GitHub Actions, no del código:
las mismas pruebas se pueden correr localmente con los pasos de arriba.

## 8. Errores comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `ModuleNotFoundError: streamlit` | Entorno virtual no activado | Activa `.venv` e instala de nuevo |
| `No such file: data/raw/...` | Ejecutar desde otra carpeta | Ejecuta desde la raíz del repo |
| Hash distinto | CSV editado o descargado de nuevo | Restaura el archivo del commit |
| La app abre pero no carga datos | CSV corrupto o incompleto | Corre `python scripts/verificar_checksums.py` |
| `streamlit` no se reconoce | Script no está en PATH | Usa `python -m streamlit run app.py` |

## 9. Qué no se reproduce

- La consulta a `datos.cali.gov.co` falla mientras dure la suspensión.
- El video requiere grabar la pantalla; el material de `video/` solo aporta
  portadas, textos y narración.
- No se incluyen correos, tokens ni credenciales.
