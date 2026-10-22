"""Capturas limpias de la app para README, Devpost y evidencia.

Uso (desde la raíz del repositorio, con la app en el puerto 8501):
    python video/capturas_app.py

Requiere:
    pip install -r video/requirements-video.txt
    python -m playwright install chromium
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / "docs" / "evidence"
APP = "http://localhost:8501"

CSS = """
header[data-testid="stHeader"], [data-testid="stToolbar"],
[data-testid="stDecoration"], #MainMenu, footer { display: none !important; }
.block-container { padding-top: 1.2rem !important; }
"""


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(APP, wait_until="domcontentloaded", timeout=90000)
        page.get_by_text("51,236").first.wait_for(timeout=90000)
        page.add_style_tag(content=CSS)
        page.wait_for_timeout(1200)
        page.screenshot(path=str(EVIDENCE / "app_home.png"))

        page.get_by_role("tab", name="Buscar mi esquina").click()
        page.wait_for_timeout(800)
        field = page.locator('input[aria-label="Escribe una calle, carrera o cruce"]')
        field.fill("")
        field.press_sequentially("CL 70 & CRA 8", delay=60)
        field.press("Enter")
        page.wait_for_timeout(3000)
        page.screenshot(path=str(EVIDENCE / "app_buscar.png"))

        try:
            page.get_by_text("Ficha y solicitud lista para radicar").click()
            page.wait_for_timeout(1200)
            page.get_by_text("Solicitud lista para radicar", exact=False).first.scroll_into_view_if_needed(timeout=4000)
            page.wait_for_timeout(800)
        except Exception:
            pass
        page.screenshot(path=str(EVIDENCE / "app_ficha.png"))

        page.get_by_role("tab", name="Trazabilidad").click()
        page.wait_for_timeout(2500)
        page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(1200)
        page.screenshot(path=str(EVIDENCE / "app_trazabilidad.png"))

        page.get_by_role("tab", name="Datos y método").click()
        page.wait_for_timeout(2500)
        page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
        page.wait_for_timeout(800)
        page.screenshot(path=str(EVIDENCE / "app_metodo.png"))
        browser.close()
    print("Capturas listas en", EVIDENCE)


if __name__ == "__main__":
    main()
