"""CicloRoto: interfaz web (Streamlit)."""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modules.alumbrado import cargar_datos, generar_panel

st.set_page_config(
    page_title="CicloRoto",
    page_icon="ðŸ”„",
    layout="wide",
)


@st.cache_data(show_spinner="Cargando datos locales...")
def _cargar():
    pqr, alum = cargar_datos()
    return pqr, alum


pqr, alum = _cargar()
panel = generar_panel(pqr, alum)
k = panel['kpis']

st.title("ðŸ”„ CicloRoto")
st.caption(
    "AuditorÃ­a de trazabilidad de la gestiÃ³n urbana de Cali â€” "
    "MÃ³dulo: Alumbrado pÃºblico"
)

# ---------------------------------------------------------------- KPIs
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("PQR 2024â€“2025", f"{k['total_pqr']:,}")
c2.metric("Proyectos de alumbrado (2017)", f"{k['total_intervenciones']:,}")
c3.metric("Puntos luminosos", f"{k['puntos_luminosos']:,}")
c4.metric("InversiÃ³n registrada", f"${k['inversion_cop'] / 1e6:,.0f} M")
c5.metric("Reportes vinculables", f"{k['vinculables']:,}")

st.warning(
    "**0 reportes son vinculables a una intervenciÃ³n de alumbrado con las "
    "fuentes pÃºblicas consultadas.** No porque las obras no existan, sino "
    "porque las fuentes no comparten clave, perÃ­odo ni identificador de caso. "
    "El mÃ³dulo mide esa brecha documental; no la interpreta como falta de obra."
)

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(
    ["ðŸ§­ DiagnÃ³stico", "ðŸ—ºï¸ Cobertura territorial", "ðŸ§¹ Calidad de datos",
     "ðŸ“š MetodologÃ­a"]
)

# ------------------------------------------------------------ DiagnÃ³stico
with tab1:
    st.subheader("Â¿Se pueden vincular los reportes con las intervenciones?")
    st.dataframe(
        panel['diagnostico'],
        width='stretch',
        hide_index=True,
    )
    st.caption(
        "Un criterio bloqueante impide atribuir un reporte a una obra concreta. "
        "Los tres bloqueos son independientes: corregir uno solo no habilita el cruce."
    )

# ------------------------------------------------------------- Cobertura
with tab2:
    st.subheader("Reportes por comuna frente a proyectos registrados en 2017")
    st.caption(
        "ComparaciÃ³n descriptiva entre aÃ±os distintos. No mide respuesta institucional "
        "ni causalidad: solo muestra quÃ© comunas tienen registro en cada fuente."
    )

    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.dataframe(
            panel['cobertura'],
            width='stretch',
            hide_index=True,
            column_config={
                'comuna': 'Comuna',
                'reportes_2024_2025': 'Reportes 2024â€“2025',
                'proyectos_2017': 'Proyectos 2017',
                'puntos_luminosos': 'Puntos luminosos',
                'inversion_cop': st.column_config.NumberColumn(
                    'InversiÃ³n (COP)', format="$ %d"
                ),
                'tiene_proyecto_2017': 'Â¿Proyecto en 2017?',
            },
        )
    with col_b:
        sin_proyecto = int((~panel['cobertura']['tiene_proyecto_2017']).sum())
        st.metric("Comunas sin proyecto en 2017", sin_proyecto)
        st.metric("Comunas con proyecto en 2017", k['comunas_con_proyectos'])
        st.metric("PQR sin comuna", f"{k['pqr_sin_comuna']:,}")
        st.caption(
            "Una comuna sin proyecto en el archivo de 2017 no implica ausencia "
            "de obras ese aÃ±o ni en aÃ±os posteriores."
        )

    st.bar_chart(
        panel['cobertura'].set_index('comuna')['reportes_2024_2025'],
        height=320,
    )

# ---------------------------------------------------------------- Calidad
with tab3:
    st.subheader("Calidad y cobertura de las fuentes")
    st.dataframe(
        panel['calidad'],
        width='stretch',
        hide_index=True,
    )
    st.caption(
        "MÃ©tricas calculadas sobre los CSV locales en data/raw. "
        "Ver docs/audit.md para el detalle de filas descartadas."
    )

# ------------------------------------------------------------ MetodologÃ­a
with tab4:
    st.subheader("MÃ©todo y lÃ­mites")
    st.markdown(
        f"""
**Fuentes**

- PQR por comuna: {k['total_pqr']:,} registros ({k['pqr_2024']:,} de 2024 y
  {k['pqr_2025']:,} de 2025). Consulta: 2026-10-19.
- Proyectos de alumbrado: {k['total_intervenciones']:,} registros de 2017,
  {k['puntos_luminosos']:,} puntos luminosos e inversiÃ³n registrada de
  ${k['inversion_cop'] / 1e6:,.0f} millones de COP. Consulta: 2026-10-19.

**Reglas aplicadas**

- Comunas normalizadas a `Comuna 1`â€“`Comuna 22` antes de cualquier comparaciÃ³n.
- Fechas fuera de 2024â€“2025 se excluyen y se reportan como faltantes.
- El perÃ­odo del alumbrado es el aÃ±o del tÃ­tulo del archivo; no se infiere
  de la columna `tipo`, que describe el tipo de obra.

**LÃ­mites**

- No existe identificador de caso en ninguna fuente.
- No hay solapamiento temporal entre reportes (2024â€“2025) e intervenciones (2017).
- La PQR no tiene categorÃ­a temÃ¡tica que aislÃ© alumbrado.
- Por lo anterior, **no se calcula atribuciÃ³n reporteâ€“obra**.
- `0 vinculables` significa "no verificable con estas fuentes", no
  "problema sin resolver".
"""
    )

st.divider()
st.caption(
    "Fuentes: datos.cali.gov.co (CKAN) Â· Consulta: 2026-10-19 Â· "
    "Datos: CC-BY Â· CÃ³digo: ver LICENSE"
)
