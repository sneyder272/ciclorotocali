"""CicloRoto Vial: interfaz web (Streamlit).

Producto principal: cruces críticos de siniestralidad vial en Cali.
Segunda capa: auditoría de trazabilidad de las obras publicadas.
"""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modules.alumbrado import cargar_datos as cargar_alumbrado
from modules.alumbrado import generar_panel as panel_alumbrado
from modules.vial import canonicalizar_cruce, cargar_datos as cargar_vial
from modules.vial import generar_ficha, generar_panel as panel_vial

st.set_page_config(
    page_title="CicloRoto Vial",
    page_icon="🔄",
    layout="wide",
)


@st.cache_data(show_spinner="Cargando siniestros viales...")
def _cargar_vial():
    return cargar_vial()


@st.cache_data(show_spinner="Cargando datos de alumbrado...")
def _cargar_alumbrado():
    return cargar_alumbrado()


vial = _cargar_vial()
pqr, alum = _cargar_alumbrado()

base = panel_vial(vial, min_registros=1)
alumbrado = panel_alumbrado(pqr, alum)
k = base['kpis']
ka = alumbrado['kpis']

st.title("🔄 CicloRoto Vial")
st.caption(
    "De la queja a la prioridad: dónde se lesiona la gente en Cali y qué "
    "no se puede verificar con los datos públicos."
)

# ------------------------------------------------------------------ KPIs
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Siniestros con lesionados", f"{k['total_registros']:,}")
c2.metric("Direcciones resolubles", f"{k['con_cruce']:,}",
          help=f"{k['pct_con_cruce']}% del total")
c3.metric("Cruces identificados", f"{k['cruces_distintos']:,}")
c4.metric("Cruce más crítico", f"{k['top_registros']}",
          help=k['top_cruce'])
c5.metric("Cruces con obra verificable", "0",
          help="Ninguna fuente pública vincula una obra con un cruce y una fecha.")

st.info(
    f"**El cruce más crítico es "
    f"{k['top_cruce'].title().replace(' Con ', ' con ')}**, con "
    f"{k['top_registros']} registros de siniestros con lesionados entre "
    f"{k['anio_min']} y {k['anio_max']}. El ranking se calcula solo con los "
    "registros cuya dirección permite identificar un cruce."
)

st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "🚦 Cruces críticos",
    "🔎 Buscar mi esquina",
    "🧭 Trazabilidad",
    "📚 Datos y método",
])

# ------------------------------------------------------- Cruces críticos
with tab1:
    f1, f2, f3 = st.columns([1, 1, 2])
    with f1:
        anios = sorted(int(a) for a in vial['anio'].dropna().unique())
        anio_sel = st.selectbox("Año", ["Todos"] + anios)
    with f2:
        mecanismos = ["Todos"] + sorted(
            m for m in vial['mecanismo'].unique() if m != 'Sin dato / otro'
        )
        mec_sel = st.selectbox("Mecanismo", mecanismos)
    with f3:
        min_reg = st.slider(
            "Mínimo de registros por cruce", min_value=3, max_value=25, value=5,
            help="Sube el mínimo para excluir cruces con muy pocos casos.",
        )

    p = panel_vial(
        vial,
        min_registros=min_reg,
        anio=None if anio_sel == "Todos" else int(anio_sel),
        mecanismo=mec_sel,
    )
    r = p['ranking']

    m1, m2, m3 = st.columns(3)
    m1.metric("Siniestros en el filtro", f"{p['total_filtrado']:,}")
    m2.metric("Cruces que superan el mínimo", f"{len(r):,}")
    m3.metric("Cobertura de dirección", f"{k['pct_con_cruce']}%")

    if r.empty:
        st.warning("No hay cruces con ese mínimo de registros. Baja el mínimo.")
    else:
        tabla = r.head(25)[[
            'puesto', 'cruce', 'registros', 'tasa_ajustada', 'ic_inferior',
            'ic_superior', 'pct_moto', 'pct_peaton', 'pct_ciclista',
            'ventana_pico', 'anios_con_registro',
        ]].rename(columns={
            'puesto': '#',
            'cruce': 'Cruce',
            'registros': 'Registros',
            'tasa_ajustada': 'Tasa ajustada',
            'ic_inferior': 'IC 95% inf.',
            'ic_superior': 'IC 95% sup.',
            'pct_moto': '% moto',
            'pct_peaton': '% peatón',
            'pct_ciclista': '% ciclista',
            'ventana_pico': 'Ventana pico',
            'anios_con_registro': 'Años con dato',
        })
        st.dataframe(tabla, width='stretch', hide_index=True)

        top10 = r.head(10).sort_values('registros')
        st.bar_chart(
            top10.set_index('cruce')['registros'],
            horizontal=True,
            height=340,
        )

        st.download_button(
            "Descargar ranking (CSV)",
            r.to_csv(index=False).encode('utf-8-sig'),
            file_name='cicloroto_cruces_criticos.csv',
            mime='text/csv',
        )

        st.caption(
            "**Tasa ajustada:** modelo jerárquico Gamma-Poisson que estabiliza "
            "conteos bajos y reporta incertidumbre. **No** corrige por volumen "
            "de tráfico, que no está publicado. Un registro es un siniestro, no "
            "una persona."
        )

# ------------------------------------------------------- Buscar esquina
with tab2:
    st.subheader("¿Qué ha pasado en tu esquina?")
    consulta = st.text_input(
        "Escribe una calle, carrera o cruce",
        placeholder="Ej: Calle 70 con Carrera 8",
        help="También acepta 'CL 70 & CRA 8' o 'calle 70 carrera 8'.",
    )

    if consulta.strip():
        canon = canonicalizar_cruce(consulta)
        texto = consulta.strip().upper()
        completo = base['ranking']

        if canon:
            exacto = completo[completo['cruce'] == canon]
        else:
            exacto = completo.iloc[0:0]

        parcial = completo[
            completo['cruce'].str.contains(texto, regex=False, na=False)
        ]

        resultados = (
            exacto if not exacto.empty else parcial
        ).head(10)

        if resultados.empty:
            st.warning(
                "No encontré ese cruce en los registros con dirección "
                "utilizable. Prueba con otra forma de escribirlo."
            )
        else:
            st.dataframe(
                resultados[[
                    'cruce', 'registros', 'pct_moto', 'pct_peaton',
                    'ventana_pico', 'anios_con_registro',
                ]].rename(columns={
                    'cruce': 'Cruce', 'registros': 'Registros',
                    'pct_moto': '% moto', 'pct_peaton': '% peatón',
                    'ventana_pico': 'Ventana pico',
                    'anios_con_registro': 'Años con dato',
                }),
                width='stretch',
                hide_index=True,
            )

            elegido = resultados.iloc[0]['cruce']
            detalle = vial[vial['cruce'] == elegido]

            d1, d2, d3, d4 = st.columns(4)
            d1.metric("Registros históricos", len(detalle))
            d2.metric("Motocicleta", f"{100 * detalle['moto'].mean():.0f}%")
            d3.metric("Peatón", f"{100 * detalle['peaton'].mean():.0f}%")
            d4.metric("Años con dato", int(detalle['anio'].nunique()))

            st.caption(
                f"Detalle de **{elegido.title().replace(' Con ', ' con ')}**"
            )
            por_hora = (
                detalle.dropna(subset=['hora_num'])
                .groupby('hora_num').size()
                .reindex(range(24), fill_value=0)
                .rename('registros')
            )
            st.bar_chart(por_hora, height=260)

            st.caption(
                "Cada barra es el número de siniestros con lesionados en esa "
                "hora, sumando todos los años disponibles. No es una predicción."
            )

            ficha = generar_ficha(detalle, elegido)
            with st.expander(
                "📄 Ficha y solicitud lista para radicar", expanded=False
            ):
                st.markdown(ficha)
                st.download_button(
                    "Descargar ficha (.md)",
                    ficha.encode('utf-8'),
                    file_name='ficha_' + elegido.lower().replace(' ', '_') + '.md',
                    mime='text/markdown',
                )
    else:
        st.caption(
            "El buscador usa la dirección textual publicada por la Secretaría "
            "de Movilidad. No hay coordenadas ni mapa."
        )

# ---------------------------------------------------------- Trazabilidad
with tab3:
    st.subheader("¿La ciudad publica si intervino en esos cruces?")
    st.markdown(
        "El ranking anterior dice **dónde** ocurren los siniestros. Para saber "
        "si la ciudad intervino ahí hace falta una obra con dirección y fecha. "
        "La única fuente de alumbrado disponible cubre **2017**, por comuna y "
        "sin identificador de caso. La PQR no tiene categoría de alumbrado."
    )

    st.dataframe(
        alumbrado['diagnostico'],
        width='stretch',
        hide_index=True,
    )

    st.warning(
        f"**{ka['vinculables']} de {ka['total_pqr']:,} reportes ciudadanos** "
        "pueden vincularse a una intervención publicada. No significa que no "
        "haya obras: significa que las fuentes no permiten verificarlo."
    )

    with st.expander("Ver cobertura territorial del alumbrado (2017)"):
        st.dataframe(
            alumbrado['cobertura'].rename(columns={
                'comuna': 'Comuna',
                'reportes_2024_2025': 'Reportes PQR 2024–2025',
                'proyectos_2017': 'Proyectos 2017',
                'puntos_luminosos': 'Puntos luminosos',
                'inversion_cop': 'Inversión (COP)',
                'tiene_proyecto_2017': '¿Proyecto en 2017?',
            }),
            width='stretch',
            hide_index=True,
        )

# --------------------------------------------------------- Datos y método
with tab4:
    st.subheader("Fuentes, modelo y límites")

    st.markdown(
        f"""
**Fuentes**

| ID | Conjunto | Registros | Período | Fuente |
|---|---|---:|---|---|
| V01 | Lesionados en accidentes de tránsito | {k['total_registros']:,} | 2016–2025 | [Secretaría de Movilidad](https://datos.cali.gov.co/dataset/75c089ba-7df3-4816-b80f-c69c6e5362ae) |
| A01 | Proyectos de alumbrado público | {ka['total_intervenciones']:,} | 2017 | [CKAN](https://datos.cali.gov.co/dataset/e6a3fd08-6a44-422f-beb7-d21ac1f38ec1) |
| A02 | PQR por comuna | {ka['total_pqr']:,} | 2024–2025 | [CKAN](https://datos.cali.gov.co/dataset/de6fa620-eda6-47c8-97ae-bcbbed493fe1) |

Todas CC-BY. Consulta: 2026-10-17 (V01) y 2026-10-19 (A01, A02).

**Cómo se construye el ranking**

1. Se normalizan las direcciones (`CRA` → `CARRERA`, `CL` → `CALLE`, etc.).
2. Se consolidan variantes del mismo cruce ordenando las dos vías:
   `CARRERA 8 CON CALLE 70` y `CALLE 70 CON CARRERA 8` son la misma esquina.
3. Se agrupa por cruce y se aplica un modelo jerárquico Gamma-Poisson
   (*empirical Bayes*) para estabilizar tasas y obtener un intervalo del 95%.
4. Se excluyen los cruces con menos registros que el mínimo elegido.

**Límites que debes saber**

- Solo **{k['pct_con_cruce']}%** de los registros tienen una dirección
  resoluble a cruce. El resto son direcciones vacías (`"."`), clínicas,
  CAI o texto no interpretable.
- **2018, 2019 y 2020 no tienen dirección** en la fuente. El ranking se
  apoya en 2016, 2017 y 2021–2025.
- 2025 está incompleto.
- No hay coordenadas ni volumen de tráfico: no se puede normalizar por
  exposición ni dibujar un mapa.
- Un registro es un **siniestro**, no una persona.
- El ranking **no** prueba que falte una obra. Prueba dónde priorizar la
  verificación y qué no se puede comprobar con lo publicado.
"""
    )

st.divider()
st.caption(
    "CicloRoto Vial · Datos: CC-BY (Alcaldía de Santiago de Cali) · "
    "Código: MIT · Consulta: 2026-10-17 / 2026-10-19"
)

