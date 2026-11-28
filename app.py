"""
Big-Data-Kuy — Dashboard Analisis Program Makan Bergizi Gratis (MBG) Indonesia 2026
Kelompok 007 • Matakuliah Big Data Analisis
"""

import streamlit as st

st.set_page_config(
    page_title="Dashboard MBG Indonesia 2026",
    page_icon="🍽️",
    layout="wide",
)

pages = [
    st.Page("page1.py", title="Beranda",      icon="🏠"),
    st.Page("page2.py", title="Data Explorer", icon="🔍"),
    st.Page("page3.py", title="Visualisasi",   icon="📊"),
    st.Page("page4.py", title="Profil Tim",    icon="👥"),
]

pg = st.navigation(pages, position="sidebar", expanded=True)

# --- Sidebar branding ---
with st.sidebar:
    st.markdown("---")
    st.caption("🍽️ **Dashboard MBG Indonesia 2026**")
    st.caption("Kelompok 007 — Big Data Analisis")
    st.caption("Danang · Nurul · Diyah")

pg.run()
