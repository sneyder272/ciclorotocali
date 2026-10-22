"""Graba la demo real de CicloRoto Vial y monta el video final.

Requisitos:
    pip install -r video/requirements-video.txt
    python -m playwright install chromium

Uso:
    python video/grabar_video.py

Salida:
    video/video_final.mp4

La app debe estar disponible en http://localhost:8501. Si no lo está, el script
la levanta con el Python actual y la cierra al terminar.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from imageio_ffmpeg import get_ffmpeg_exe
from playwright.sync_api import sync_playwright


BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
APP = "http://localhost:8501"
REPO = "https://github.com/sneyder272/ciclorotocali"
FFMPEG = get_ffmpeg_exe()

# Duraciones de la narración (es-CO-GonzaloNeural), en segundos.
AUDIOS = [
    ("01_gancho.mp3", 24.7),
    ("02_problema.mp3", 24.8),
    ("03_que_construimos.mp3", 32.4),
    ("04a_busqueda.mp3", 12.4),
    ("04b_datos.mp3", 19.2),
    ("04c_ficha.mp3", 24.0),
    ("05_trazabilidad.mp3", 33.1),
    ("06_cierre.mp3", 25.9),
    ("07_creditos.mp3", 10.0),
]
GAP = 1.0
TITLE = 3.0
CREDITS = 11.5
APP_LEN = 200.0
TOTAL = TITLE + APP_LEN + CREDITS

CSS = """
header[data-testid="stHeader"], [data-testid="stToolbar"],
[data-testid="stDecoration"], #MainMenu, footer { display: none !important; }
.block-container { padding-top: 1.2rem !important; }
"""


def _url_ok(url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=2) as r:
            return r.read().decode("utf-8", "ignore").strip() == "ok"
    except Exception:
        return False


def ensure_app() -> subprocess.Popen | None:
    if _url_ok(f"{APP}/_stcore/health"):
        print("App ya disponible en", APP)
        return None
    print("Levantando Streamlit...")
    proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py",
         "--server.port", "8501", "--server.headless", "true"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(60):
        time.sleep(1)
        if _url_ok(f"{APP}/_stcore/health"):
            print("App lista.")
            return proc
    proc.terminate()
    raise RuntimeError("Streamlit no respondió en 60 s.")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    nombres = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for nombre in nombres:
        if Path(nombre).exists():
            return ImageFont.truetype(nombre, size)
    return ImageFont.load_default(size=size)


def make_credits() -> Path:
    destino = BASE / "creditos.png"
    img = Image.new("RGB", (1920, 1080), "#0B1F33")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([120, 120, 1800, 960], radius=34, outline="#24445F", width=3)
    d.text((960, 300), "CicloRoto Vial", font=font(96, True),
           fill="#F5F7FA", anchor="mm")
    d.text((960, 400), "De la queja a la prioridad", font=font(40),
           fill="#9FB3C8", anchor="mm")
    d.rounded_rectangle([650, 490, 1270, 570], radius=22, fill="#F2B705")
    d.text((960, 530), "Narración con IA (edge-tts)", font=font(30, True),
           fill="#0B1F33", anchor="mm")
    d.text((960, 660), "Datos: CC-BY · Alcaldía de Santiago de Cali",
           font=font(30), fill="#F5F7FA", anchor="mm")
    d.text((960, 720), "Código: MIT", font=font(30), fill="#F5F7FA", anchor="mm")
    d.text((960, 810), "github.com/sneyder272/ciclorotocali",
           font=font(28), fill="#9FB3C8", anchor="mm")
    d.text((960, 880), "51,236 registros · 16 pruebas · 0 vínculos verificables",
           font=font(24), fill="#9FB3C8", anchor="mm")
    img.save(destino)
    return destino


def scroll(page, dy: int, pasos: int = 4) -> None:
    for _ in range(pasos):
        page.mouse.wheel(0, dy // pasos)
        page.wait_for_timeout(120)


def record_app() -> tuple[Path, float]:
    clips = BASE / "_clips"
    if clips.exists():
        shutil.rmtree(clips)
    clips.mkdir(parents=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(clips),
            record_video_size={"width": 1920, "height": 1080},
        )
        page = context.new_page()
        video = page.video
        t0 = time.monotonic()
        page.goto(APP, wait_until="domcontentloaded", timeout=90000)
        page.get_by_text("51,236").first.wait_for(timeout=90000)
        load_offset = time.monotonic() - t0
        page.add_style_tag(content=CSS)
        page.wait_for_timeout(500)

        t_start = time.monotonic()

        def at(sec: float) -> None:
            restante = sec - (time.monotonic() - t_start)
            if restante > 0:
                page.wait_for_timeout(restante * 1000)

        # Escena 1: gancho, buscar la esquina.
        at(1.0)
        page.get_by_role("tab", name="Buscar mi esquina").click()
        at(1.4)
        campo = page.locator('input[aria-label="Escribe una calle, carrera o cruce"]')
        campo.fill("")
        campo.press_sequentially("CL 70 & CRA 8", delay=90)
        campo.press("Enter")
        at(5.5)
        scroll(page, 260, 4)

        # Escena 2: problema y límites. Se adelanta el clic porque Streamlit
        # tarda unos segundos en repintar la pestaña.
        at(18.5)
        page.get_by_role("tab", name="Datos y método").click()
        at(19.4)
        try:
            page.get_by_text("Límites que debes saber", exact=False).first.scroll_into_view_if_needed(timeout=4000)
        except Exception:
            scroll(page, 600, 5)

        # Escena 3: cruces críticos.
        at(44.5)
        page.get_by_role("tab", name="Cruces críticos").click()
        at(45.4)
        page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
        try:
            page.get_by_text("¿Cómo leer esta tabla?").click()
        except Exception:
            pass
        at(46.5)
        scroll(page, 420, 5)

        # Escena 4a: buscar de nuevo.
        at(78.0)
        page.get_by_role("tab", name="Buscar mi esquina").click()
        at(78.6)
        page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
        campo = page.locator('input[aria-label="Escribe una calle, carrera o cruce"]')
        campo.fill("")
        campo.press_sequentially("CL 70 & CRA 8", delay=90)
        campo.press("Enter")

        # Escena 4b: leer los datos.
        at(95.3)
        scroll(page, 520, 5)
        at(100.0)
        scroll(page, 280, 4)

        # Escena 4c: ficha y solicitud.
        at(111.5)
        try:
            page.get_by_text("Ficha y solicitud lista para radicar").click()
        except Exception:
            pass
        at(113.0)
        scroll(page, 620, 6)
        at(115.5)
        scroll(page, 420, 4)

        # Escena 5: trazabilidad.
        at(136.5)
        page.get_by_role("tab", name="Trazabilidad").click()
        at(137.6)
        page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
        scroll(page, 380, 5)
        at(141.5)
        try:
            page.get_by_text("Ver cobertura territorial del alumbrado (2017)").click()
        except Exception:
            pass
        at(143.5)
        scroll(page, 320, 4)

        # Escena 6: método y repositorio.
        at(170.5)
        page.get_by_role("tab", name="Datos y método").click()
        at(171.6)
        page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
        scroll(page, 520, 5)
        at(173.5)
        scroll(page, 360, 4)
        at(182.0)
        try:
            page.goto(REPO, wait_until="domcontentloaded", timeout=60000)
            page.get_by_text("CicloRoto Vial", exact=False).first.wait_for(timeout=30000)
            at(188.0)
            scroll(page, 380, 4)
        except Exception:
            print("No se pudo abrir GitHub; se mantiene la app.")
        at(APP_LEN + 0.5)

        context.close()
        browser.close()
        ruta = Path(video.path())
        destino = clips / "app.webm"
        if ruta.exists() and ruta != destino:
            ruta.replace(destino)
        elif destino.exists():
            pass
        else:
            candidatos = list(clips.glob("*.webm"))
            if not candidatos:
                raise RuntimeError("Playwright no generó video.")
            candidatos[0].replace(destino)
        print(f"Grabación: {destino.name} ({destino.stat().st_size / 1e6:.1f} MB), "
              f"offset de carga: {load_offset:.2f} s")
        return destino, load_offset


def ffmpeg(args: list[str], descripcion: str) -> None:
    print(descripcion)
    r = subprocess.run([FFMPEG, "-y", *args], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-4000:])
        raise RuntimeError(f"ffmpeg falló: {descripcion}")


def build_audio() -> Path:
    salida = BASE / "narracion.wav"
    cmd: list[str] = []
    for nombre, _ in AUDIOS:
        cmd += ["-i", str(BASE / "es-CO-GonzaloNeural" / nombre)]
    filtro = ""
    for i in range(len(AUDIOS)):
        if i < len(AUDIOS) - 1:
            filtro += f"[{i}:a]aresample=48000,apad=pad_dur={GAP}[a{i}];"
        else:
            filtro += f"[{i}:a]aresample=48000[a{i}];"
    filtro += "".join(f"[a{i}]" for i in range(len(AUDIOS)))
    filtro += f"concat=n={len(AUDIOS)}:v=0:a=1[out]"
    ffmpeg(
        [*cmd, "-filter_complex", filtro, "-map", "[out]",
         "-ar", "48000", "-ac", "2", str(salida)],
        "Montando narración...",
    )
    return salida


def build_video(app: Path, load_offset: float, credits: Path) -> Path:
    title_seg = BASE / "_clips" / "title.mp4"
    app_seg = BASE / "_clips" / "app.mp4"
    credits_seg = BASE / "_clips" / "credits.mp4"
    silencioso = BASE / "_clips" / "silencioso.mp4"
    final = BASE / "video_final.mp4"

    base_vf = (
        "scale=1920:1080:force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p,fps=30"
    )
    ffmpeg(
        ["-loop", "1", "-framerate", "30", "-i", str(BASE / "portada_1920x1080.png"),
         "-t", str(TITLE), "-vf", base_vf + ",fade=t=in:st=0:d=0.6",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-pix_fmt", "yuv420p", "-an", str(title_seg)],
        "Creando portada...",
    )
    inicio = max(0.4, min(1.8, load_offset - 0.35))
    ffmpeg(
        ["-i", str(app), "-ss", f"{inicio:.2f}", "-t", str(APP_LEN),
         "-vf", base_vf + ",fade=t=in:st=0:d=0.5",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-pix_fmt", "yuv420p", "-an", str(app_seg)],
        "Preparando demo...",
    )
    ffmpeg(
        ["-loop", "1", "-framerate", "30", "-i", str(credits),
         "-t", str(CREDITS), "-vf", base_vf + ",fade=t=in:st=0:d=0.6",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-pix_fmt", "yuv420p", "-an", str(credits_seg)],
        "Creando créditos...",
    )

    lista = BASE / "_clips" / "concat.txt"
    lista.write_text(
        "\n".join(f"file '{p.as_posix()}'" for p in (title_seg, app_seg, credits_seg)) + "\n",
        encoding="utf-8",
    )
    ffmpeg(
        ["-f", "concat", "-safe", "0", "-i", str(lista),
         "-c", "copy", str(silencioso)],
        "Uniendo escenas...",
    )

    audio = build_audio()
    ffmpeg(
        ["-i", str(silencioso), "-i", str(audio),
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-shortest", "-movflags", "+faststart", str(final)],
        "Añadiendo narración...",
    )
    return final


def main() -> int:
    proc = ensure_app()
    try:
        credits = make_credits()
        app, load_offset = record_app()
        final = build_video(app, load_offset, credits)
        print(f"\nLISTO: {final}")
        print(f"Duración objetivo: {TOTAL:.1f} s ({TOTAL / 60:.1f} min)")
        print("Revisa el video antes de subirlo a YouTube.")
        return 0
    finally:
        if proc is not None:
            proc.terminate()
            proc.wait(timeout=10)


if __name__ == "__main__":
    raise SystemExit(main())
