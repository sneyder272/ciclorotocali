# Devpost — copy exacto (English)

> Reemplaza el texto viejo. Las cifras anteriores (248 proyectos, 748 brechas,
> 5 pruebas) eran de la versión de alumbrado y ya no corresponden al producto.
> No las dejes en la submission.

## Project name

```text
CicloRoto Vial
```

## Elevator pitch

```text
Turns 51,236 road-injury records from Cali into a ranked list of critical intersections and a ready-to-file request — and shows what public data cannot verify.
```

## Project Story (Markdown)

```markdown
## Inspiration

Cali publishes thousands of road-injury records with the address written as free text. It also publishes public-lighting projects and citizen requests (PQR). Each dataset is useful on its own, but they share no case ID, no per-record date in the lighting file, and no common geographic key.

We wanted to answer a practical question: **can a neighbor verify whether the city has intervened at the corner where people are getting hurt?**

That question led to CicloRoto Vial: a civic-data tool that turns 51,236 injury records into a ranked list of critical intersections, and then shows — without inventing the missing link — what cannot be verified with the data the city currently publishes.

## What it does

CicloRoto Vial has two connected layers.

**1. Road safety (main product).** It processes 51,236 injury records from Cali's Secretaría de Movilidad (2016–2025), normalizes free-text addresses, consolidates variants of the same intersection, and ranks intersections with a hierarchical Gamma-Poisson model. The ranking reports an adjusted rate and a 95% interval, so a handful of crashes does not look like a stable rate.

- 28,411 records (55.5%) resolve to an intersection.
- 9,261 distinct intersections; 1,228 have at least 5 records.
- The most critical intersection is **Calle 70 con Carrera 8**: 148 injury records, 41.2% flag a motorcycle and 12.8% flag a pedestrian, with a peak window of 16:00–18:59.
- For any intersection, the app generates a brief and a **ready-to-file information request** based on Colombia's right-of-petition law (Ley 1755 de 2015).

**2. Traceability (accountability layer).** It compares 17,642 citizen requests (2024–2025) with 247 public-lighting projects (2017). The result is **0 linkable records**. Not because there were no projects, but because the sources do not share a key, the lighting dataset has no date per record, and the periods do not overlap. The zero is a documented data gap, not proof of neglect.

## How we built it

Python and pandas for ingestion, address normalization, and entity resolution (`CRA`/`CARR`/`KR` → `CARRERA`, `CL`/`CLL` → `CALLE`, separators `CON`, `Y`, `&`, `/`, and no-connector formats). We sort the two streets in each address so `CARRERA 8 CON CALLE 70` and `CALLE 70 CON CARRERA 8` become the same intersection.

The ranking uses an empirical-Bayes Gamma-Poisson model with a method-of-moments prior. It shrinks small counts and returns a 95% interval without adding a scipy dependency.

The interface is Streamlit: four tabs, CSV download, and a Markdown brief. Sixteen pytest tests cover exact counts, normalization, filters, the brief, and the rendered app. The CSV files are in the repository, so the app runs offline.

## Challenges

- **Addresses, not coordinates.** Only 55.5% of records resolve to an intersection. The rest are `"."`, clinics, police stations, or unparseable text. We report the coverage instead of imputing locations.
- **Three years without addresses.** 2018, 2019, and 2020 have `"."` in 100% of records (16,616 rows). The ranking relies on 2016, 2017, and 2021–2025, and the app says so.
- **A zero that is not a conclusion.** An early version derived the lighting period from a column that did not contain dates. That produced spurious gaps. We removed the artifact and documented the discard. The honest result is "not verifiable," not "no project."
- **Performance.** Computing the peak window per intersection took minutes. We vectorized it with a contingency table; the app now loads in under a second.

## What we learned

The most valuable result of a civic-data project is not always the answer. Sometimes it is a well-documented limit: "these sources cannot link an intervention to this intersection and date." That limit is more useful than an invented map.

We also learned to keep code and data licenses separate: MIT for the code, CC-BY for the data. And to make uncertainty part of the interface, not a footnote.

## What's next

- Add traffic exposure so the ranking can normalize by vehicles or pedestrians.
- Add coordinates when the city publishes them, enabling a map without inferring locations.
- Connect the brief to the city's virtual petition channel.
- Extend the traceability engine to road maintenance and traffic signals when a source with address and date per intervention exists.

## Sources

- Injury records: Secretaría de Movilidad de Cali, 51,236 rows, 2016–2025, CC-BY, consulted 2026-10-17.
- Public lighting: 247 projects, 2017, CC-BY, consulted 2026-10-19.
- PQR: 17,642 records, 2024–2025, CC-BY, consulted 2026-10-19.

**Honesty note:** an unmatched request does not prove that the problem is unresolved. The ranking does not prove that an intervention is missing, and it does not establish causation. A record is a crash, not a person.
```

## Built with

```text
Python, pandas, NumPy, Streamlit, pytest, GitHub Actions, Git, GitHub, open data, civic technology, data visualization, statistical modeling, Gamma-Poisson, empirical Bayes, address parsing, entity resolution
```

## Try it out

```text
https://github.com/sneyder272/ciclorotocali
```

## Video demo

Paste the YouTube URL after recording. The script, narration, and cover are in
`docs/video_script.md` and `video_cicloroto/`.

## Additional info — What is the specific problem, and how do you know it's real?

```text
The specific problem: in Cali, a resident can suspect that a corner is dangerous, but cannot verify whether the city has intervened there. The city publishes road-injury records with free-text addresses, public-lighting projects by commune and year, and citizen requests without a lighting category or case ID. The datasets cannot be joined at the case or address level.

How we know it is real (public data, not assumptions):
- 51,236 injury records (2016–2025) from the Secretaría de Movilidad. Only 28,411 (55.5%) have an address that resolves to an intersection; 2018–2020 have "." in 100% of rows (16,616 records).
- 247 public-lighting projects (2017) and 17,642 PQR (2024–2025). They share no case ID, the lighting file has no per-record date, and the periods do not overlap. Cross-matching yields 0 linkable records.
- The most critical intersection, Calle 70 con Carrera 8, has 148 injury records.

We did not conduct interviews or field validation that we cannot demonstrate. The evidence is the open data itself, its coverage, and its gaps. That is why the tool does not claim a project is missing; it shows that the link is not verifiable with what is published.
```

## Team email

Fill in the email you want organizers to use. Do not commit it to the public
repository.

## Media

Upload `video_cicloroto/portada_1500x1000.png` (3:2, recommended by Devpost).
If you prefer the 16:9 version, use `portada_1280x720.png`.

## Final checklist

- [ ] Project name is **CicloRoto Vial**, not CICLOROTOCALI.
- [ ] No mention of 248 projects, 748 gaps, or 5 tests.
- [ ] Built with tags: no duplicates, 25 max.
- [ ] Try it out link has no `.git` suffix.
- [ ] Video is 2–6 minutes and shows the app working.
- [ ] AI narration is disclosed in the description.
- [ ] Team email is correct and private.
