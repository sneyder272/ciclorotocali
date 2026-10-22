# Tomas y montaje del video

**Objetivo:** 3:34 en el corte automatizado actual, 1920 × 1080, 30 fps, MP4 H.264.
**Voz:** `es-CO-GonzaloNeural` (3:26) o `es-CO-SalomeNeural` (3:52).
**Corte ya generado:** `video/video_final.mp4`, creado por `video/grabar_video.py`.
Esta tabla sirve para rehacerlo a mano si se prefiere.
**Regla:** la pantalla debe ser una grabación real de la app; no se simulan
resultados ni se editan cifras.

## Antes de grabar

- [ ] App corriendo en `http://localhost:8501` con `python -m streamlit run app.py`.
- [ ] Navegador en 125–150 % de zoom, barra de marcadores oculta.
- [ ] Perfil limpio: sin correo, WhatsApp, Telegram, notificaciones ni pestañas personales.
- [ ] No mostrar correo del equipo, tokens, rutas con el nombre de usuario ni claves.
- [ ] Cerrar el micrófono: el video se graba **sin audio** y luego se monta la narración.
- [ ] Ensayar una vez con cronómetro. Si pasa de 4:30, recortar la escena de método.
- [ ] Grabar por escenas y nombrar los clips igual que el audio (`01_gancho.mp4`, etc.).

## Tomas exactas

| # | Clip | Audio | Inicio | Duración | Acción en pantalla |
|---:|---|---|---:|---:|---|
| 1 | `01_gancho.mp4` | `01_gancho.mp3` | 0:00 | 24.7 s | 3 s de portada; luego app arriba; clic en **Buscar mi esquina**; escribir `CL 70 & CRA 8`; dejar visible el resultado con **148** |
| 2 | `02_problema.mp4` | `02_problema.mp3` | 0:27 | 24.8 s | **Datos y método**; bajar a **Límites**; señalar 55.5 %, 2018–2020 sin dirección y “no hay coordenadas” |
| 3 | `03_que_construimos.mp4` | `03_que_construimos.mp3` | 0:54 | 32.4 s | **Cruces críticos**; mover el mínimo 5 → 10 → 5; cambiar año a 2024 y volver a Todos; dejar la tabla y el top 5 |
| 4 | `04a_busqueda.mp4` | `04a_busqueda.mp3` | 1:28 | 12.4 s | **Buscar mi esquina**; borrar y escribir despacio `CL 70 & CRA 8`; mostrar la fila canónica **CALLE 70 CON CARRERA 8** |
| 5 | `04b_datos.mp4` | `04b_datos.mp3` | 1:42 | 19.2 s | Bajar a las métricas: 148, 41 % moto, 13 % peatón, años con dato; mostrar el gráfico por hora y la ventana 16:00–18:59 |
| 6 | `04c_ficha.mp4` | `04c_ficha.mp3` | 2:04 | 24.0 s | Abrir **Ficha y solicitud lista para radicar**; bajar hasta la advertencia de que no prueba que falte una obra y hasta la Ley 1755; señalar **Descargar ficha (.md)** |
| 7 | `05_trazabilidad.mp4` | `05_trazabilidad.mp3` | 2:30 | 33.1 s | **Trazabilidad**; señalar el aviso **0 de 17,642**; mostrar la tabla de diagnóstico; abrir **cobertura territorial del alumbrado (2017)** y volver |
| 8 | `06_cierre.mp4` | `06_cierre.mp3` | 3:05 | 25.9 s | **Datos y método**; tabla de fuentes; cortar a GitHub (README); cortar a terminal con `pytest -q` y **16 passed**; volver al título |
| 9 | `07_creditos.mp4` | `07_creditos.mp3` | 3:33 | 10.0 s | Portada; rótulo **Narración con IA (edge-tts)**; “Código MIT · Datos CC-BY” y URL del repo |

Deja **1–2 s de silencio** entre clips. El corte automatizado queda en **3:34**;
con pausas manuales más largas puede llegar a **3:45–4:00**.
Si usas la voz de Salomé, los inicios se corren ~25 s; conserva el orden y los
silencios.

## Tomas de apoyo (5–8 s)

1. Primer plano del KPI **0 cruces con obra verificable**.
2. Scroll lento del top 10 de cruces.
3. Clic en **Descargar ranking (CSV)** y mostrar el archivo descargado.
4. `python scripts/verificar_checksums.py` con los tres `OK`.
5. `docs/evidence/sources.md` y la captura del comunicado del portal.
6. Estructura del repo en GitHub: `app.py`, `modules/`, `data/raw/`, `tests/`.

## Montaje en CapCut

1. Proyecto **1920 × 1080, 30 fps**.
2. Video en la pista 1; cada MP3 al inicio de su clip, en la pista 2.
3. Sin música, o música instrumental a −25 dB. Si no tienes licencia clara, sin música.
4. Subtítulos automáticos en español; corregir a mano `51.236`, `148`, `17.642`,
   `Calle 70 con Carrera 8` y `Ley 1755 de 2015`.
5. Rótulo pequeño al inicio o al final: **Narración con IA (edge-tts)**.
6. Exportar **MP4, H.264, 1080p, 30 fps**. Revisar que dure entre 2 y 6 minutos.
7. Subir a YouTube como **público o no listado**; comprobar que el enlace abre
   sin iniciar sesión. Pegar la URL en Devpost.

## Privacidad y honestidad

- No muestres nombres, cédulas, correos ni direcciones personales.
- No inventes una obra, una entrevista ni una validación de campo.
- El video muestra la app y el repositorio reales; la narración es sintética y
  se declara.
- Si una cifra no coincide con la app, no la ocultes: corrige la edición o
  vuelve a grabar la toma.
