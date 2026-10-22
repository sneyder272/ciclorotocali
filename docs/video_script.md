# Guion del video — CicloRoto Vial

**Duración objetivo:** 3:34 en el corte actual (límite: 6:00)
**Formato:** 1920×1080, 30 fps, MP4 H.264
**Voz:** narración sintética en español colombiano (`edge-tts`), sin rostro ni avatar. Se declara como IA en el video y en la submission.
**Regla:** cada cifra que se dice existe en la app o en `docs/audit.md`.

---

## Antes de grabar

- [ ] Cerrar WhatsApp, Telegram, correo y notificaciones del sistema (No molestar).
- [ ] Navegador en 125–150 % de zoom para que el texto se lea en 1080p.
- [ ] Barra de marcadores oculta; pestañas solo con la app y el repositorio.
- [ ] App abierta en `http://localhost:8501`, pestaña **Buscar mi esquina**.
- [ ] Ensayar una vez con cronómetro. Si pasa de 4:30, recortar la sección de método.
- [ ] Grabar el video **sin audio**; la narración se monta después.
- [ ] Revisar que no aparezca ningún nombre, cédula ni correo real.

**Narración ya generada:** no necesitas hablar. Hay dos voces sintéticas en
`video/` (cortes por escena). Instrucciones de montaje en
`video/LEEME.md` y transcripción en `docs/transcript.md`. Agrega el
rótulo **“Narración con IA (edge-tts)”** y dilo en la descripción de la
submission.

---

## 0:00 – 0:25 · Gancho

**Pantalla:** título y tabla (3 s). Cortar a **Buscar mi esquina**, escribir
`CL 70 & CRA 8` y mostrar el resultado de **148** mientras termina el gancho.
Así el producto se entiende en los primeros 20 segundos.

> En Cali se registraron **51,236 siniestros con lesionados** entre 2016 y 2025.
> La ciudad publica la dirección de cada uno, aunque solo el **55 %** se puede
> ubicar en un cruce. Y no publica si intervino en esa esquina.
>
> CicloRoto Vial convierte esos datos en un ranking de cruces críticos y en una
> ficha con la solicitud lista para radicar.

## 0:25 – 1:00 · El problema

**Pantalla:** pestaña **Datos y método**, sección de límites.

> El problema tiene dos capas. Primero, la información existe pero está
> dispersa: direcciones escritas de mil formas, sin coordenadas, y tres años
> completos sin dirección.
>
> Segundo, aunque un vecino sepa que su esquina es peligrosa, no puede verificar
> si pidió una obra, si se ejecutó o si existe un estudio de seguridad vial.
> No es que no haya datos: es que no se pueden cruzar.

## 1:00 – 1:45 · Qué construimos

**Pantalla:** volver a **Cruces críticos**; mover el filtro de mínimo y el año.

> La primera capa es siniestralidad vial: **51,236 registros** de la Secretaría
> de Movilidad, de 2016 a 2025. Normalizamos las direcciones, consolidamos
> variantes del mismo cruce y aplicamos un modelo jerárquico **Gamma-Poisson**
> para estabilizar conteos bajos y reportar un intervalo de confianza.
>
> La segunda capa audita las obras publicadas: **247 proyectos de alumbrado de
> 2017** y **17,642 PQR de 2024 y 2025**.

## 1:45 – 3:15 · Demo: buscar mi esquina

**Pantalla:** pestaña **Buscar mi esquina**. Escribir despacio
`CL 70 & CRA 8`. Mostrar el resultado. Bajar al gráfico por hora.
Abrir el expander **Ficha y solicitud lista para radicar**.

> Voy a buscar mi esquina. Escribo “CL 70 & CRA 8”. La app la reconoce y la
> convierte en **“CALLE 70 CON CARRERA 8”**: la misma esquina, escrita de otra
> forma.
>
> Es el cruce más crítico: **148 siniestros con lesionados** en los años con
> dirección utilizable. Cuarenta y uno por ciento involucra motocicleta; trece
> por ciento, peatón. La ventana con más casos es de **4 a 7 de la tarde**.
> Debajo está el detalle por hora y los años con dato.
>
> Ahora abro la ficha. Incluye los indicadores y una advertencia: **no puedo
> afirmar que falte una obra**. Lo que sí puedo hacer es pedir la información.
> La ficha trae una solicitud redactada, con el fundamento en la Ley 1755 de
> 2015, lista para descargar y radicar en la Ventanilla Única.
>
> Ese es el flujo completo: del dato a la acción.

## 3:15 – 4:05 · La segunda capa

**Pantalla:** pestaña **Trazabilidad**. Señalar el aviso amarillo y la tabla de
diagnóstico.

> La segunda capa responde la otra pregunta: ¿la ciudad publica si intervino en
> ese cruce?
>
> Cruzamos los 17,642 reportes ciudadanos con los 247 proyectos de alumbrado.
> El resultado es **cero vinculables**. No porque no haya obras, sino porque las
> fuentes no comparten clave, no tienen identificador de caso y el alumbrado
> solo cubre 2017, mientras las PQR son de 2024 y 2025.
>
> Ese cero es el hallazgo: una **brecha de datos**, no una prueba de abandono.

## 4:05 – 4:45 · Método y cierre

**Pantalla:** pestaña **Datos y método**; luego el repositorio en GitHub
(README y `pytest`). Cerrar con el título de la app.

> El proyecto es reproducible: los CSV están en el repositorio, la app corre sin
> internet y **16 pruebas** verifican los conteos, la normalización y la ficha.
> No usamos datos inventados ni afirmamos causalidad.
>
> El ranking dice **dónde priorizar**. La ficha dice **qué preguntar**.
>
> CicloRoto Vial: de la queja a la prioridad. Repositorio y demo en el enlace de
> la submission.

---

## Tomas de apoyo (opcionales, 5–8 s cada una)

1. Primer plano del KPI **0 cruces con obra verificable**.
2. Scroll lento de la tabla top 10.
3. Descarga del CSV del ranking.
4. `pytest -q` terminando en **16 passed**.
5. `docs/audit.md` con la tabla de cobertura por año (2018–2020 en 0 %).

## Frases que NO se deben decir

- “La ciudad no ha hecho nada en ese cruce.”
- “Estas obras causaron menos accidentes.”
- “El 55 % restante no tiene accidentes.”
- “CicloRoto predice dónde ocurrirá el próximo siniestro.”

## Después de grabar

- [ ] Duración entre 2:00 y 6:00.
- [ ] 1080p real (no un video 720p escalado).
- [ ] Audio sin clipping; voz por encima de la música (si hay).
- [ ] Sin notificaciones, nombres ni correos visibles.
- [ ] Exportar MP4 y subir a YouTube; pegar el enlace en Devpost.
- [ ] Verificar que el enlace no sea privado.
