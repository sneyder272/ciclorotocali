# Impacto y teoría de cambio

## El cambio que buscamos

Hoy un vecino puede intuir que su esquina es peligrosa, pero no tiene un número
ni sabe a quién preguntar. CicloRoto Vial convierte esa intuición en tres cosas
concretas: **un conteo**, **una ficha** y **una solicitud**.

## Tres usuarios, tres acciones

| Usuario | Qué hace | Qué obtiene | Qué cambia |
|---|---|---|---|
| Vecino o vecina | Busca su esquina | 148 siniestros, % moto/peatón, ventana horaria | Pasa de la queja a una solicitud con fundamento |
| Autoridad o periodista | Filtra el ranking y descarga el CSV | 1,228 cruces priorizados | Deja de elegir por percepción |
| Organización comunitaria | Lee el diagnóstico de trazabilidad | 0 de 17,642 reportes vinculables | Pide obras con dirección, fecha e ID de caso |

## Escala del problema (datos reales)

- **51,236** siniestros con lesionados (2016–2025).
- **28,411** direcciones resolubles a un cruce (**55.5 %**).
- **9,261** cruces identificados; **1,228** con 5 o más registros.
- **148** siniestros en el cruce más crítico (Calle 70 con Carrera 8).
- **0 de 17,642** reportes ciudadanos vinculables a una obra publicada.

No se trata de que haya 9,261 problemas distintos. Se trata de que hoy no
existe una lista pública y priorizada; el proyecto la construye con lo que la
ciudad ya publica.

## Cómo se mediría el impacto (sin inventar métricas)

**Indicadores de adopción** (requieren instrumentación, no se afirman hoy):
búsquedas por cruce, fichas descargadas, solicitudes radicadas.

**Indicadores de resultado** (verificables con datos públicos):
- número de intervenciones publicadas con dirección, fecha e identificador;
- número de solicitudes respondidas;
- número de cruces del top 20 con una intervención verificable.

**Condición de falsificación:** si la ciudad ya publicara intervenciones
vinculables a un cruce y una fecha, el hallazgo “0 vinculables” sería falso. La
app muestra exactamente qué fuentes se cruzaron y qué campos faltan, para que
cualquiera pueda refutarlo.

## Lo que este proyecto no afirma

- No prueba que falte una obra.
- No prueba que una intervención haya reducido los siniestros.
- No cubre el 100 % de los siniestros: solo el 55.5 % con dirección resoluble.
- No dibuja un mapa: no hay coordenadas publicadas.
- No reemplaza una auditoría de seguridad vial.

## Por qué puede escalar

- El pipeline es modular: un nuevo conjunto con dirección y fecha se puede
  incorporar sin reescribir el ranking.
- El modelo Gamma-Poisson funciona con cualquier conteo por entidad.
- La ficha y la solicitud son plantillas reutilizables por comuna o por tipo de
  intervención.
- La app corre sin internet y sin servidor: un computador con Python basta.

## Costo de mantenerlo

- Un CSV y una app; no hay base de datos ni servicio en la nube.
- Las pruebas (16) verifican los conteos y la normalización en menos de 20
  segundos.
- El costo real está en conseguir datos vinculables, no en la infraestructura.
