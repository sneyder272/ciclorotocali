"""Genera la narración del video con voces neuronales en español colombiano.

Requiere: pip install edge-tts mutagen
Uso: python generar_narracion.py

Salida:
  textos/*.txt                 texto hablado por escena
  es-CO-GonzaloNeural/*.mp3    narración masculina
  es-CO-SalomeNeural/*.mp3     narración femenina
"""
import asyncio
from pathlib import Path

import edge_tts
from mutagen.mp3 import MP3

SECCIONES = {
    "01_gancho": (
        "En Cali se registraron 51 mil 236 siniestros con lesionados entre "
        "2016 y 2025. La ciudad publica la dirección de cada uno, aunque solo "
        "el 55 por ciento se puede ubicar en un cruce. Y no publica si "
        "intervino en esa esquina. CicloRoto Vial convierte esos datos en un "
        "ranking de cruces críticos y en una ficha con la solicitud lista "
        "para radicar."
    ),
    "02_problema": (
        "El problema tiene dos capas. Primero, la información existe pero "
        "está dispersa: direcciones escritas de mil formas, sin coordenadas, "
        "y tres años completos sin dirección. Segundo, aunque un vecino sepa "
        "que su esquina es peligrosa, no puede verificar si pidió una obra, "
        "si se ejecutó o si existe un estudio de seguridad vial. No es que no "
        "haya datos: es que no se pueden cruzar."
    ),
    "03_que_construimos": (
        "La primera capa es siniestralidad vial: 51 mil 236 registros de la "
        "Secretaría de Movilidad, de 2016 a 2025. Normalizamos las "
        "direcciones, consolidamos variantes del mismo cruce y aplicamos un "
        "modelo jerárquico Gamma Poisson para estabilizar conteos bajos y "
        "reportar un intervalo de confianza. La segunda capa audita las obras "
        "publicadas: 247 proyectos de alumbrado de 2017 y 17 mil 642 PQR de "
        "2024 y 2025."
    ),
    "04a_busqueda": (
        "Voy a buscar mi esquina. Escribo CL 70 y CRA 8. La app la reconoce y "
        "la convierte en Calle 70 con Carrera 8: la misma esquina, escrita de "
        "otra forma."
    ),
    "04b_datos": (
        "Es el cruce más crítico: 148 siniestros con lesionados en los años "
        "con dirección utilizable. Cuarenta y uno por ciento involucra "
        "motocicleta; trece por ciento, peatón. La ventana con más casos es de "
        "4 a 7 de la tarde. Debajo está el detalle por hora y los años con "
        "dato."
    ),
    "04c_ficha": (
        "Ahora abro la ficha. Incluye los indicadores y una advertencia: no "
        "puedo afirmar que falte una obra. Lo que sí puedo hacer es pedir la "
        "información. La ficha trae una solicitud redactada, con el fundamento "
        "en la Ley 1755 de 2015, lista para descargar y radicar en la "
        "Ventanilla Única. Ese es el flujo completo: del dato a la acción."
    ),
    "05_trazabilidad": (
        "La segunda capa responde la otra pregunta: ¿la ciudad publica si "
        "intervino en ese cruce? Cruzamos los 17 mil 642 reportes ciudadanos "
        "con los 247 proyectos de alumbrado. El resultado es cero "
        "vinculables. No porque no haya obras, sino porque las fuentes no "
        "comparten clave, no tienen identificador de caso y el alumbrado solo "
        "cubre 2017, mientras las PQR son de 2024 y 2025. Ese cero es el "
        "hallazgo: una brecha de datos, no una prueba de abandono."
    ),
    "06_cierre": (
        "El proyecto es reproducible: los CSV están en el repositorio, la app "
        "corre sin internet y 16 pruebas verifican los conteos, la "
        "normalización y la ficha. No usamos datos inventados ni afirmamos "
        "causalidad. El ranking dice dónde priorizar. La ficha dice qué "
        "preguntar. CicloRoto Vial: de la queja a la prioridad. Repositorio y "
        "demo en el enlace de la submission."
    ),
    "07_creditos": (
        "Narración generada con inteligencia artificial. Datos abiertos de la "
        "Alcaldía de Cali, licencia CC BY. Código MIT."
    ),
}

VOCES = ["es-CO-GonzaloNeural", "es-CO-SalomeNeural"]
RATE = "-5%"


async def main() -> None:
    base = Path(__file__).resolve().parent
    textos = base / "textos"
    textos.mkdir(exist_ok=True)

    for nombre, texto in SECCIONES.items():
        (textos / f"{nombre}.txt").write_text(texto, encoding="utf-8")

    totales = {}
    for voz in VOCES:
        carpeta = base / voz
        carpeta.mkdir(exist_ok=True)
        total = 0.0
        for nombre, texto in SECCIONES.items():
            destino = carpeta / f"{nombre}.mp3"
            await edge_tts.Communicate(texto, voz, rate=RATE).save(str(destino))
            duracion = MP3(destino).info.length
            total += duracion
            print(f"{voz}  {nombre}: {duracion:5.1f}s")
        totales[voz] = total
        print(f"{voz}  TOTAL: {total:.1f}s ({total / 60:.1f} min)\n")

    print("Listo. Elige una voz y monta los MP3 en orden sobre la grabación.")


if __name__ == "__main__":
    asyncio.run(main())
