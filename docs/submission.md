# Postulación — Neighborhood Hacks 2026

## Título

**CicloRoto Vial — De la queja a la prioridad**

## Tagline (una línea)

Convierte 51,236 siniestros viales de Cali en un ranking de cruces críticos y en
una solicitud lista para radicar. Y muestra, sin inventar, qué no se puede
verificar con los datos públicos.

## Inspiración

Cali publica los siniestros viales con la dirección en texto. También publica
obras y reportes ciudadanos. Pero un vecino que quiere saber si su esquina es
peligrosa —y si la ciudad intervino allí— termina leyendo tres conjuntos de
datos que no comparten clave, no comparten fecha y no tienen identificador de
caso.

No quisimos construir otro mapa bonito. Quisimos cerrar el recorrido completo:
**saber dónde ocurre, entender qué falta y salir con una acción concreta**.

## Qué hace

CicloRoto Vial tiene dos capas conectadas.

**1. Siniestralidad vial (producto principal).**
Procesa 51,236 registros de siniestros con lesionados (2016–2025) de la
Secretaría de Movilidad. Normaliza direcciones escritas de formas distintas,
consolida variantes del mismo cruce (`CARRERA 8 CON CALLE 70` =
`CALLE 70 CON CARRERA 8`) y produce:

- un ranking de cruces con tasa ajustada e intervalo de confianza del 95 %
  (modelo jerárquico Gamma-Poisson);
- filtros por año, mecanismo y mínimo de registros;
- un buscador que acepta `CL 70 & CRA 8`, `calle 70 con carrera 8` o
  `calle 70 carrera 8`;
- una **ficha descargable** por cruce con indicadores, ventana horaria y una
  **solicitud de información lista para radicar** (Ley 1755 de 2015).

**2. Trazabilidad de obras (capa de accountability).**
Cruza los 17,642 reportes ciudadanos (PQR 2024–2025) con los 247 proyectos de
alumbrado público (2017). El resultado es **0 vinculables**: no porque no haya
obras, sino porque las fuentes no permiten vincularlas. El proyecto hace visible
esa brecha en lugar de rellenarla con una suposición.

## Cómo lo construimos

- **Python + pandas** para la ingesta y la normalización de direcciones
  (`CRA`/`CARR`/`KR` → `CARRERA`, `CL`/`CLL` → `CALLE`, separadores `CON`, `Y`,
  `&`, `/`, `ESQUINA` y formato sin conector).
- **Resolución de entidades**: se ordenan las dos vías de cada cruce para que
  las variantes cuenten como una sola esquina.
- **Modelo Gamma-Poisson (empirical Bayes)** con previa estimada por momentos:
  estabiliza conteos bajos y reporta incertidumbre sin depender de scipy.
- **Streamlit** para la interfaz, con cuatro pestañas, descarga de CSV y ficha
  en Markdown.
- **pytest**: 16 pruebas sobre conteos exactos, normalización, filtros, ficha y
  renderizado de la app.
- Los CSV viven en el repositorio; la app abre **sin internet**.

## Retos

- **Direcciones, no coordenadas.** Solo el **55.5 %** de los registros (28,411)
  se resuelven a un cruce. El resto son `"."`, clínicas, CAI o texto no
  interpretable. En lugar de imputar, el ranking declara la cobertura.
- **Tres años sin dirección.** 2018, 2019 y 2020 tienen `"."` en el 100 % de los
  registros (16,616 filas). El ranking se apoya en 2016, 2017 y 2021–2025, y
  así se muestra en la app.
- **Un cero que no es una conclusión.** Al principio el cruce PQR–alumbrado
  producía brechas falsas porque el período del alumbrado se derivaba de una
  columna que no contenía fechas. Lo corregimos y documentamos el descarte en
  `docs/audit.md`. Hoy el resultado honesto es “no verificable”, no “sin obra”.
- **Rendimiento.** El cálculo de la ventana horaria por grupo tardaba minutos.
  Lo vectorizamos con una tabla de contingencia y la app pasó de ~4 minutos a
  menos de un segundo.

## Logros

- **51,236** siniestros procesados; **28,411** direcciones resueltas;
  **9,261** cruces identificados.
- El cruce más crítico, **Calle 70 con Carrera 8**, acumula **148** siniestros
  con lesionados; 41 % involucra motocicleta y 13 % peatón.
- **1,228** cruces superan el mínimo de 5 registros.
- **16/16** pruebas en verde; instalación limpia verificada desde un clon nuevo.
- Un flujo completo en menos de 30 segundos: escribir la esquina → ver el
  riesgo → descargar la ficha → radicar la solicitud.

## Qué aprendimos

Que el dato más valioso de un proyecto cívico no siempre es el que responde una
pregunta: a veces es el que **delimita lo que no se puede responder**. Un cero
bien documentado —“estas fuentes no permiten vincular una obra con este cruce”—
es más útil que un mapa inventado.

También aprendimos a separar licencias: **MIT** para el código y **CC-BY** para
los datos. La licencia de los datos no cubre el código ni viceversa.

## Qué sigue

- Incorporar el volumen de tráfico para normalizar por exposición.
- Añadir coordenadas cuando la ciudad las publique, para habilitar un mapa sin
  inferir ubicaciones.
- Conectar la ficha con el canal virtual de la Ventanilla Única.
- Extender el motor de trazabilidad a otros sectores (malla vial, semáforos)
  cuando exista una fuente con dirección y fecha por intervención.

## Tecnologías

Python, pandas, NumPy, Streamlit, pytest, Git/GitHub. Datos abiertos CC-BY de
la Alcaldía de Santiago de Cali.

## Enlaces

- Repositorio: https://github.com/sneyder272/ciclorotocali
- Demo local: `python -m streamlit run app.py` → `http://localhost:8501`
- Metodología y auditoría: `docs/audit.md`
- Guion del video: `docs/video_script.md`

## Uso de IA

La asistencia de IA se usó para exploración, redacción y revisión de código.
Todas las cifras se calculan desde los CSV locales y se verifican con `pytest`;
no se inventaron datos, fuentes, entrevistas ni validaciones.

## Nota de honestidad

El ranking **no** prueba que falte una obra ni que una intervención haya
reducido los siniestros. Indica dónde priorizar la verificación y qué
información hace falta para comprobarlo. Un registro es un **siniestro**, no una
persona.
