"""
Page 1: Beranda — Ringkasan Dashboard Program MBG Indonesia 2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# ── Load data ──────────────────────────────────────────────────
FILE_PATH = "bigdata_kelompok.csv"

@st.cache_data
def load_data():
    return pd.read_csv(FILE_PATH)

df = load_data()

# ── Header ─────────────────────────────────────────────────────
st.title("🍽️ Dashboard Program Makan Bergizi Gratis (MBG)")
st.markdown(
    "**Analisis Data Distribusi Makanan Bergizi Gratis Nasional Indonesia 2026**  \n"
    "Dashboard ini menyajikan analisis komprehensif terhadap **{:,}** titik distribusi "
    "di **{}** provinsi seluruh Indonesia.".format(len(df), df["province"].nunique())
)

st.markdown("---")

# ── KPI Metrics Row 1 ─────────────────────────────────────────
st.subheader("📌 Ringkasan Indikator Utama")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Titik Distribusi",
        value=f"{len(df):,}",
    )
with col2:
    st.metric(
        label="Provinsi Tercakup",
        value=f"{df['province'].nunique()}",
    )
with col3:
    avg_cost = df["total_meal_cost_idr"].mean()
    st.metric(
        label="Rata-rata Biaya/Porsi",
        value=f"Rp{avg_cost:,.0f}",
    )
with col4:
    avg_cal = df["estimated_calories_kcal"].mean()
    st.metric(
        label="Rata-rata Kalori/Porsi",
        value=f"{avg_cal:,.0f} kkal",
    )

# ── KPI Metrics Row 2 ─────────────────────────────────────────
col5, col6, col7, col8 = st.columns(4)

with col5:
    avg_protein = df["estimated_protein_grams"].mean()
    st.metric(
        label="Rata-rata Protein/Porsi",
        value=f"{avg_protein:.1f} gram",
    )
with col6:
    avg_waste = df["plate_waste_percentage"].mean()
    st.metric(
        label="Rata-rata Sisa Makanan",
        value=f"{avg_waste:.1f}%",
    )
with col7:
    avg_attendance = df["student_attendance_rate_pct"].mean()
    st.metric(
        label="Rata-rata Kehadiran Siswa",
        value=f"{avg_attendance:.1f}%",
    )
with col8:
    avg_local = df["local_farmer_sourcing_pct"].mean()
    st.metric(
        label="Rata-rata Serapan Petani Lokal",
        value=f"{avg_local:.1f}%",
    )

st.markdown("---")

# ── Compliance Tier Overview ───────────────────────────────────
st.subheader("🏅 Distribusi Tier Kepatuhan Program")

tier_labels = {
    "Exemplary-Gold-Standard": "🥇 Exemplary (Gold)",
    "Standard-Compliant": "✅ Standard Compliant",
    "Marginal-Quality-At-Risk": "⚠️ Marginal (At Risk)",
    "Non-Compliant-Intervention-Required": "🚨 Non-Compliant",
}
tier_colors = {
    "🥇 Exemplary (Gold)": "#2ecc71",
    "✅ Standard Compliant": "#3498db",
    "⚠️ Marginal (At Risk)": "#f39c12",
    "🚨 Non-Compliant": "#e74c3c",
}

tier_counts = df["bgn_program_compliance_tier"].value_counts().reset_index()
tier_counts.columns = ["tier", "count"]
tier_counts["label"] = tier_counts["tier"].map(tier_labels)
tier_counts["pct"] = (tier_counts["count"] / tier_counts["count"].sum() * 100).round(1)

col_chart, col_detail = st.columns([2, 1])

with col_chart:
    fig_tier = px.pie(
        tier_counts,
        names="label",
        values="count",
        color="label",
        color_discrete_map=tier_colors,
        hole=0.45,
    )
    fig_tier.update_traces(textposition="outside", textinfo="percent+label")
    fig_tier.update_layout(
        showlegend=False,
        margin=dict(t=20, b=20, l=20, r=20),
        height=350,
    )
    st.plotly_chart(fig_tier, use_container_width=True)

with col_detail:
    for _, row in tier_counts.sort_values("count", ascending=False).iterrows():
        st.markdown(f"**{row['label']}**")
        st.markdown(f"&emsp;{row['count']:,} distribusi ({row['pct']}%)")

st.markdown("---")

# ── Top 10 Provinces by Distribution Count ─────────────────────
st.subheader("🗺️ 10 Provinsi dengan Titik Distribusi Terbanyak")

prov_counts = df["province"].value_counts().head(10).reset_index()
prov_counts.columns = ["province", "count"]

fig_prov = px.bar(
    prov_counts,
    x="count",
    y="province",
    orientation="h",
    color="count",
    color_continuous_scale="Blues",
    text="count",
)
fig_prov.update_layout(
    yaxis=dict(autorange="reversed", title=""),
    xaxis_title="Jumlah Titik Distribusi",
    coloraxis_showscale=False,
    margin=dict(t=10, b=30),
    height=400,
)
fig_prov.update_traces(textposition="outside")
st.plotly_chart(fig_prov, use_container_width=True)

st.markdown("---")

# ── About the Data ─────────────────────────────────────────────
st.subheader("📄 Tentang Dataset")
st.markdown(
    """
Dataset ini memuat data operasional program **Makan Bergizi Gratis (MBG)** Indonesia 2026
yang mencakup informasi distribusi makanan ke berbagai kategori penerima manfaat di seluruh
provinsi Indonesia. Setiap record merepresentasikan satu paket distribusi dengan detail:

- **Logistik**: jarak pengiriman, moda transportasi, waktu transit, suhu kedatangan
- **Biaya**: biaya bahan baku, total biaya per porsi, biaya efektif setelah penyesuaian sisa makanan
- **Nutrisi**: estimasi kalori, protein, rasio biaya terhadap nutrisi
- **Kepatuhan**: tier compliance BGN, indeks risiko pembusukan, pemicu sisa makanan
- **Dampak Ekonomi**: persentase serapan petani lokal, skor multiplier ekonomi lokal
    """
)
