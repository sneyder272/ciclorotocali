# Video de CicloRoto Vial

Esta carpeta contiene todo lo necesario para montar el video sin hablar:
portadas, textos, narraciones sintéticas y los scripts que las generan. La
grabación de pantalla debe ser real; los MP3 solo aportan la voz.

## Contenido

```text
video/
├── LEEME.md
├── generar_narracion.py          # regenera textos y MP3 con edge-tts
├── generar_portada.py            # regenera portadas con Pillow (Windows)
├── textos/                       # texto exacto de cada escena
├── es-CO-GonzaloNeural/          # voz masculina, 3:26 en total
├── es-CO-SalomeNeural/           # voz femenina, 3:52 en total
├── portada_1920x1080.png         # portada del video
├── portada_1280x720.png          # alternativa 16:9
└── portada_1500x1000.png         # imagen 3:2 para Devpost
```

## Escenas y duración

| Archivo | Escena | Gonzalo | Salomé |
|---|---|---:|---:|
| `01_gancho.mp3` | Gancho | 24.7 s | 27.5 s |
| `02_problema.mp3` | El problema | 24.8 s | 28.3 s |
| `03_que_construimos.mp3` | Qué construimos | 32.4 s | 37.3 s |
| `04a_busqueda.mp3` | Buscar la esquina | 12.4 s | 13.7 s |
| `04b_datos.mp3` | Leer los datos | 19.2 s | 21.7 s |
| `04c_ficha.mp3` | Abrir la ficha | 24.0 s | 26.8 s |
| `05_trazabilidad.mp3` | Segunda capa | 33.1 s | 37.8 s |
| `06_cierre.mp3` | Cierre | 25.9 s | 28.9 s |
| `07_creditos.mp3` | Créditos y licencias | 10.0 s | 10.7 s |

Escucha las dos y elige. Gonzalo suena más neutro; Salomé, más cálida. No hace
falta usar la voz del autor.

## Montaje

1. Sigue la tabla de tomas de [`../docs/shot_list.md`](../docs/shot_list.md).
2. Graba la pantalla **sin audio** (OBS, Clipchamp o Win+G), en 1080p y 30 fps.
3. En CapCut: proyecto 1920 × 1080, 30 fps; video en la pista 1; cada MP3 al
   inicio de su escena en la pista 2; 1–2 s de silencio entre bloques.
4. Subtítulos automáticos en español; corrige a mano `51.236`, `148`,
   `17.642`, `Calle 70 con Carrera 8` y `Ley 1755 de 2015`.
5. Añade el rótulo **Narración con IA (edge-tts)** al inicio o al final.
6. Exporta MP4 H.264, 1080p, 30 fps. Debe durar entre 2 y 6 minutos.
7. Súbelo a YouTube (público o no listado), comprueba que abre sin login y pega
   la URL en Devpost.

## Regenerar la narración (opcional)

Requiere internet y las dependencias:

```bash
pip install edge-tts mutagen
python generar_narracion.py
```

El script sobrescribe `textos/` y las dos carpetas de MP3. No requiere cuenta.
La voz es sintética; se declara en la submission y en el video.

## Regenerar las portadas (opcional)

```bash
pip install pillow
python generar_portada.py
```

El script usa las fuentes de Windows (`C:/Windows/Fonts/arial*.ttf`). En Linux
o macOS, cambia `FONT_BOLD` y `FONT_REG` por una fuente instalada. Las portadas
ya están incluidas; no es necesario regenerarlas para el video.

## Reglas del hackathon

- El video debe durar **2–6 minutos** y mostrar el proyecto funcionando.
- El uso de IA está permitido, pero **debe declararse**.
- No inventes una demo: la grabación debe ser de la app real.
- No muestres correos, nombres, cédulas, tokens ni notificaciones personales.
