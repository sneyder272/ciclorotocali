"""Verifica los SHA-256 de los CSV crudos contra docs/evidence/checksums.sha256."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKSUMS = ROOT / "docs" / "evidence" / "checksums.sha256"


def main() -> int:
    if not CHECKSUMS.exists():
        print(f"No existe {CHECKSUMS}")
        return 1

    errores = 0
    lineas = 0
    for linea in CHECKSUMS.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea:
            continue
        esperado, relativo = linea.split("  ", 1)
        ruta = ROOT / relativo
        if not ruta.exists():
            print(f"FALTA  {relativo}")
            errores += 1
            continue
        actual = hashlib.sha256(ruta.read_bytes()).hexdigest()
        if actual == esperado:
            print(f"OK  {relativo}")
        else:
            print(f"ERROR  {relativo}")
            print(f"  esperado: {esperado}")
            print(f"  actual:   {actual}")
            errores += 1
        lineas += 1

    print(f"{lineas} archivos verificados.")
    return 1 if errores else 0


if __name__ == "__main__":
    raise SystemExit(main())
