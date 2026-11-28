"""
Page 4: Profil Tim — Anggota Kelompok 007
"""

import streamlit as st

st.title("👥 Profil Tim — Kelompok 007")
st.markdown("Tim pengembang Dashboard Analisis Program MBG Indonesia 2026")

st.markdown("---")

# ── Team Members ───────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        ### 🧑‍💻 Danang
        **Peran:** Data Analyst & Backend Developer

        **Kontribusi:**
        - Pengolahan dan pembersihan dataset MBG
        - Pengembangan halaman Data Explorer
        - Analisis statistik deskriptif

        **Tools:** Python, Pandas, Git
        """
    )

with col2:
    st.markdown(
        """
        ### 👩‍💻 Nurul
        **Peran:** Project Lead & Frontend Developer

        **Kontribusi:**
        - Inisialisasi repository GitHub
        - Pengembangan halaman Beranda & Dashboard
        - Desain layout dan navigasi aplikasi

        **Tools:** Streamlit, Plotly, GitHub
        """
    )

with col3:
    st.markdown(
        """
        ### 👩‍💻 Diyah
        **Peran:** Visualization Specialist

        **Kontribusi:**
        - Perancangan visualisasi data interaktif
        - Pengembangan halaman Visualisasi
        - Deployment ke Streamlit Cloud

        **Tools:** Plotly, Matplotlib, Streamlit Cloud
        """
    )

st.markdown("---")

# ── Project Info ───────────────────────────────────────────────
st.subheader("📋 Informasi Proyek")

st.markdown(
    """
| Item | Detail |
|------|--------|
| **Mata Kuliah** | Big Data Analisis (ELA6105) |
| **Kelompok** | 007 |
| **Semester** | Ganjil 2026/2027 |
| **Dataset** | Data Distribusi Program Makan Bergizi Gratis (MBG) Indonesia 2026 |
| **Jumlah Data** | 13.000 titik distribusi di 38 provinsi |
| **Teknologi** | Python, Streamlit, Pandas, Plotly |
| **Repository** | [github.com/nurulqurannn/Big-Data-Kuy](https://github.com/nurulqurannn/Big-Data-Kuy) |
    """
)

st.markdown("---")

# ── Tech Stack ─────────────────────────────────────────────────
st.subheader("🛠️ Teknologi yang Digunakan")

col_t1, col_t2, col_t3, col_t4 = st.columns(4)

with col_t1:
    st.markdown("**🐍 Python**\n\nBahasa pemrograman utama untuk pengolahan data dan pengembangan web app.")

with col_t2:
    st.markdown("**📊 Plotly**\n\nLibrary visualisasi interaktif untuk membuat grafik dan chart yang dinamis.")

with col_t3:
    st.markdown("**🌊 Streamlit**\n\nFramework web app untuk data science yang mudah dan cepat.")

with col_t4:
    st.markdown("**🐙 GitHub**\n\nPlatform kolaborasi dan version control untuk manajemen kode sumber.")

st.markdown("---")
st.caption("© 2026 Kelompok 007 — Big Data Analisis")
