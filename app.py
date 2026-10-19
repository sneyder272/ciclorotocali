"""CicloRoto: Interfaz web (Streamlit)."""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.alumbrado import cargar_datos, generar_panel

st.set_page_config(
    page_title="CicloRoto",
    page_icon="🔄",
    layout="wide",
)

st.title("🔄 CicloRoto")
st.caption("Plataforma de trazabilidad de gestión urbana — Módulo: Alumbrado")

# Cargar datos
with st.spinner("Cargando datos reales..."):
    pqr, alum = cargar_datos()
    panel = generar_panel(pqr, alum)

# KPIs
kpis = panel['kpis']
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("PQR Reportados", f"{kpis['total_pqr']:,}")
c2.metric("Intervenciones Alumbrado", f"{kpis['total_intervenciones']:,}")
c3.metric("Comunas con PQR", kpis['comunas_con_pqr'])
c4.metric("Brechas Identificadas", kpis['brechas_identificadas'])
c5.metric("Reportes sin Intervención", f"{kpis['total_brecha_reportes']:,}")

st.divider()

# Pestañas
tab1, tab2, tab3 = st.tabs(["📊 Trazabilidad", "🔍 Brechas Verificables", "📈 Análisis"])

with tab1:
    st.subheader("Trazabilidad por Comuna y Período")
    st.dataframe(panel['trazabilidad'], use_container_width=True)

with tab2:
    st.subheader("Brechas Verificables")
    st.caption("Zonas con reportes pero sin intervención vinculada en las fuentes consultadas")
    st.dataframe(panel['brechas'], use_container_width=True)

with tab3:
    st.subheader("Análisis por Comuna")
    comunas = panel['trazabilidad'].groupby('comuna').agg({
        'total_reportes': 'sum',
        'total_intervenciones': 'sum',
        'brecha': 'sum'
    }).reset_index()
    st.dataframe(comunas, use_container_width=True)

st.divider()
st.caption("Fuentes: datos.cali.gov.co (CKAN) | Fecha de consulta: 2026-10-19 | Licencia: CC-BY")
