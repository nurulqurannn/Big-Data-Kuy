"""
Page 3: Visualisasi — Grafik dan Analisis Visual Data MBG
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Load data ──────────────────────────────────────────────────
FILE_PATH = "bigdata_kelompok.csv"

@st.cache_data
def load_data():
    return pd.read_csv(FILE_PATH)

df = load_data()

st.title("📊 Visualisasi Data MBG")
st.markdown("Eksplorasi visual terhadap data program Makan Bergizi Gratis Indonesia 2026.")

# ── Province filter in sidebar ─────────────────────────────────
st.sidebar.markdown("### 🎛️ Filter Visualisasi")
all_provinces = sorted(df["province"].unique())
selected_provinces = st.sidebar.multiselect(
    "Filter Provinsi (kosongkan = semua)",
    options=all_provinces,
    default=[],
    placeholder="Semua provinsi",
    key="viz_prov",
)

viz_df = df.copy()
if selected_provinces:
    viz_df = viz_df[viz_df["province"].isin(selected_provinces)]

st.sidebar.markdown(f"*{len(viz_df):,} data ditampilkan*")

st.markdown("---")

# ═══════════════════════════════════════════════════════════════
# SECTION 1: Distribusi per Provinsi
# ═══════════════════════════════════════════════════════════════
st.subheader("1️⃣ Distribusi Titik MBG per Provinsi")

prov_data = viz_df["province"].value_counts().reset_index()
prov_data.columns = ["Provinsi", "Jumlah"]

fig1 = px.bar(
    prov_data.head(15),
    x="Provinsi",
    y="Jumlah",
    color="Jumlah",
    color_continuous_scale="Viridis",
    text="Jumlah",
)
fig1.update_layout(
    xaxis_tickangle=-45,
    coloraxis_showscale=False,
    margin=dict(t=10, b=80),
    height=450,
)
fig1.update_traces(textposition="outside")
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════
# SECTION 2: Compliance Tier per Provinsi (Stacked Bar)
# ═══════════════════════════════════════════════════════════════
st.subheader("2️⃣ Tier Kepatuhan BGN per Provinsi")

tier_order = [
    "Exemplary-Gold-Standard",
    "Standard-Compliant",
    "Marginal-Quality-At-Risk",
    "Non-Compliant-Intervention-Required",
]
tier_colors_map = {
    "Exemplary-Gold-Standard": "#2ecc71",
    "Standard-Compliant": "#3498db",
    "Marginal-Quality-At-Risk": "#f39c12",
    "Non-Compliant-Intervention-Required": "#e74c3c",
}

prov_tier = (
    viz_df.groupby(["province", "bgn_program_compliance_tier"])
    .size()
    .reset_index(name="count")
)

# Top 15 provinces by count
top_provs = viz_df["province"].value_counts().head(15).index.tolist()
prov_tier_top = prov_tier[prov_tier["province"].isin(top_provs)]

fig2 = px.bar(
    prov_tier_top,
    x="province",
    y="count",
    color="bgn_program_compliance_tier",
    color_discrete_map=tier_colors_map,
    category_orders={"bgn_program_compliance_tier": tier_order},
    barmode="stack",
    labels={"province": "Provinsi", "count": "Jumlah", "bgn_program_compliance_tier": "Tier"},
)
fig2.update_layout(
    xaxis_tickangle=-45,
    legend_title="Tier Kepatuhan",
    margin=dict(t=10, b=80),
    height=500,
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════
# SECTION 3: Kategori Penerima Manfaat
# ═══════════════════════════════════════════════════════════════
st.subheader("3️⃣ Distribusi Kategori Penerima Manfaat")

col_a, col_b = st.columns(2)

with col_a:
    ben_data = viz_df["beneficiary_category"].value_counts().reset_index()
    ben_data.columns = ["Kategori", "Jumlah"]
    fig3a = px.pie(
        ben_data,
        names="Kategori",
        values="Jumlah",
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.4,
    )
    fig3a.update_traces(textposition="inside", textinfo="percent+label")
    fig3a.update_layout(showlegend=False, margin=dict(t=10, b=10), height=400)
    st.plotly_chart(fig3a, use_container_width=True)

with col_b:
    # Average cost per beneficiary category
    ben_cost = viz_df.groupby("beneficiary_category")["total_meal_cost_idr"].mean().reset_index()
    ben_cost.columns = ["Kategori", "Rata-rata Biaya (Rp)"]
    ben_cost = ben_cost.sort_values("Rata-rata Biaya (Rp)", ascending=True)

    fig3b = px.bar(
        ben_cost,
        x="Rata-rata Biaya (Rp)",
        y="Kategori",
        orientation="h",
        color="Rata-rata Biaya (Rp)",
        color_continuous_scale="Oranges",
        text=ben_cost["Rata-rata Biaya (Rp)"].apply(lambda x: f"Rp{x:,.0f}"),
    )
    fig3b.update_layout(
        coloraxis_showscale=False,
        margin=dict(t=10, b=10),
        height=400,
        yaxis_title="",
        xaxis_title="Rata-rata Biaya per Porsi (Rp)",
    )
    fig3b.update_traces(textposition="outside")
    st.plotly_chart(fig3b, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════
# SECTION 4: Scatter — Biaya vs Kalori
# ═══════════════════════════════════════════════════════════════
st.subheader("4️⃣ Hubungan Biaya per Porsi vs Kandungan Kalori")

fig4 = px.scatter(
    viz_df,
    x="total_meal_cost_idr",
    y="estimated_calories_kcal",
    color="bgn_program_compliance_tier",
    color_discrete_map=tier_colors_map,
    category_orders={"bgn_program_compliance_tier": tier_order},
    opacity=0.5,
    size="estimated_protein_grams",
    size_max=12,
    labels={
        "total_meal_cost_idr": "Total Biaya per Porsi (Rp)",
        "estimated_calories_kcal": "Estimasi Kalori (kkal)",
        "bgn_program_compliance_tier": "Tier Kepatuhan",
        "estimated_protein_grams": "Protein (g)",
    },
    hover_data=["province", "beneficiary_category"],
)
fig4.update_layout(
    legend_title="Tier Kepatuhan",
    margin=dict(t=10, b=30),
    height=500,
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════
# SECTION 5: Food Waste Analysis
# ═══════════════════════════════════════════════════════════════
st.subheader("5️⃣ Analisis Sisa Makanan (Food Waste)")

col_w1, col_w2 = st.columns(2)

with col_w1:
    st.markdown("**Pemicu Utama Sisa Makanan**")
    waste_driver = viz_df["primary_food_waste_driver"].value_counts().reset_index()
    waste_driver.columns = ["Pemicu", "Jumlah"]
    fig5a = px.bar(
        waste_driver,
        x="Jumlah",
        y="Pemicu",
        orientation="h",
        color="Pemicu",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        text="Jumlah",
    )
    fig5a.update_layout(
        showlegend=False,
        margin=dict(t=10, b=10),
        height=350,
        yaxis_title="",
    )
    fig5a.update_traces(textposition="outside")
    st.plotly_chart(fig5a, use_container_width=True)

with col_w2:
    st.markdown("**Rata-rata Sisa Makanan per Klaster Wilayah**")
    waste_cluster = (
        viz_df.groupby("regional_cluster")["plate_waste_percentage"]
        .mean()
        .reset_index()
        .sort_values("plate_waste_percentage", ascending=False)
    )
    waste_cluster.columns = ["Klaster", "Avg Waste (%)"]
    fig5b = px.bar(
        waste_cluster,
        x="Klaster",
        y="Avg Waste (%)",
        color="Avg Waste (%)",
        color_continuous_scale="Reds",
        text=waste_cluster["Avg Waste (%)"].apply(lambda x: f"{x:.1f}%"),
    )
    fig5b.update_layout(
        coloraxis_showscale=False,
        margin=dict(t=10, b=80),
        height=350,
        xaxis_tickangle=-25,
    )
    fig5b.update_traces(textposition="outside")
    st.plotly_chart(fig5b, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════
# SECTION 6: Jenis Protein
# ═══════════════════════════════════════════════════════════════
st.subheader("6️⃣ Distribusi Jenis Protein & Biaya")

col_p1, col_p2 = st.columns(2)

with col_p1:
    protein_counts = viz_df["protein_type"].value_counts().reset_index()
    protein_counts.columns = ["Jenis Protein", "Jumlah"]
    fig6a = px.pie(
        protein_counts,
        names="Jenis Protein",
        values="Jumlah",
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    fig6a.update_traces(textposition="inside", textinfo="percent+label")
    fig6a.update_layout(showlegend=False, margin=dict(t=10, b=10), height=400)
    st.plotly_chart(fig6a, use_container_width=True)

with col_p2:
    protein_cost = (
        viz_df.groupby("protein_type")["raw_ingredient_cost_per_portion_idr"]
        .mean()
        .reset_index()
        .sort_values("raw_ingredient_cost_per_portion_idr", ascending=True)
    )
    protein_cost.columns = ["Jenis Protein", "Avg Biaya Bahan (Rp)"]
    fig6b = px.bar(
        protein_cost,
        x="Avg Biaya Bahan (Rp)",
        y="Jenis Protein",
        orientation="h",
        color="Avg Biaya Bahan (Rp)",
        color_continuous_scale="Greens",
        text=protein_cost["Avg Biaya Bahan (Rp)"].apply(lambda x: f"Rp{x:,.0f}"),
    )
    fig6b.update_layout(
        coloraxis_showscale=False,
        margin=dict(t=10, b=10),
        height=400,
        yaxis_title="",
    )
    fig6b.update_traces(textposition="outside")
    st.plotly_chart(fig6b, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════
# SECTION 7: Moda Transportasi
# ═══════════════════════════════════════════════════════════════
st.subheader("7️⃣ Moda Transportasi & Risiko Pembusukan")

transport_risk = (
    viz_df.groupby("delivery_transport_mode")
    .agg(
        avg_distance=("delivery_distance_km", "mean"),
        avg_transit=("transit_time_minutes", "mean"),
        avg_spoilage=("spoilage_risk_index", "mean"),
        count=("distribution_id", "count"),
    )
    .reset_index()
    .sort_values("avg_spoilage", ascending=False)
)

fig7 = px.scatter(
    transport_risk,
    x="avg_transit",
    y="avg_spoilage",
    size="count",
    color="delivery_transport_mode",
    size_max=50,
    labels={
        "avg_transit": "Rata-rata Waktu Transit (menit)",
        "avg_spoilage": "Rata-rata Indeks Risiko Pembusukan",
        "delivery_transport_mode": "Moda Transportasi",
        "count": "Jumlah Distribusi",
    },
    hover_data=["avg_distance"],
)
fig7.update_layout(
    legend_title="Moda Transportasi",
    margin=dict(t=10, b=30),
    height=450,
)
st.plotly_chart(fig7, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════
# SECTION 8: Heatmap — Avg Cost per Province × Beneficiary
# ═══════════════════════════════════════════════════════════════
st.subheader("8️⃣ Heatmap: Rata-rata Biaya per Provinsi × Kategori Penerima")

heatmap_data = (
    viz_df.pivot_table(
        index="province",
        columns="beneficiary_category",
        values="total_meal_cost_idr",
        aggfunc="mean",
    )
    .round(0)
)

# Only top 20 provinces for readability
top20 = viz_df["province"].value_counts().head(20).index.tolist()
heatmap_data = heatmap_data.loc[heatmap_data.index.isin(top20)]

fig8 = px.imshow(
    heatmap_data,
    color_continuous_scale="YlOrRd",
    aspect="auto",
    labels={"x": "Kategori Penerima", "y": "Provinsi", "color": "Avg Biaya (Rp)"},
    text_auto=".0f",
)
fig8.update_layout(
    margin=dict(t=10, b=80),
    height=600,
    xaxis_tickangle=-30,
)
st.plotly_chart(fig8, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════
# SECTION 9: Dampak Ekonomi Lokal
# ═══════════════════════════════════════════════════════════════
st.subheader("9️⃣ Dampak Ekonomi Lokal per Klaster Wilayah")

econ_cluster = (
    viz_df.groupby("regional_cluster")
    .agg(
        avg_local_sourcing=("local_farmer_sourcing_pct", "mean"),
        avg_econ_multiplier=("local_economic_multiplier_score", "mean"),
    )
    .reset_index()
)

fig9 = go.Figure()
fig9.add_trace(go.Bar(
    x=econ_cluster["regional_cluster"],
    y=econ_cluster["avg_local_sourcing"],
    name="Avg Serapan Petani Lokal (%)",
    marker_color="#27ae60",
    text=econ_cluster["avg_local_sourcing"].apply(lambda x: f"{x:.1f}%"),
    textposition="outside",
))
fig9.add_trace(go.Bar(
    x=econ_cluster["regional_cluster"],
    y=econ_cluster["avg_econ_multiplier"] * 10,  # scale to comparable range
    name="Avg Skor Multiplier (×10)",
    marker_color="#2980b9",
    text=econ_cluster["avg_econ_multiplier"].apply(lambda x: f"{x:.1f}"),
    textposition="outside",
))
fig9.update_layout(
    barmode="group",
    margin=dict(t=10, b=80),
    height=450,
    xaxis_tickangle=-20,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig9, use_container_width=True)

# ── Correlation Heatmap ────────────────────────────────────────
st.markdown("---")
st.subheader("🔟 Korelasi Antar Variabel Numerik")

num_cols = [
    "total_meal_cost_idr", "estimated_calories_kcal", "estimated_protein_grams",
    "plate_waste_percentage", "spoilage_risk_index", "delivery_distance_km",
    "transit_time_minutes", "food_arrival_temperature_celsius",
    "student_attendance_rate_pct", "local_farmer_sourcing_pct",
    "local_economic_multiplier_score",
]
corr = viz_df[num_cols].corr().round(2)

short_labels = [
    "Biaya", "Kalori", "Protein", "Waste%", "Spoilage",
    "Jarak", "Transit", "Suhu", "Kehadiran", "Petani Lokal", "Multiplier",
]

fig10 = px.imshow(
    corr,
    x=short_labels,
    y=short_labels,
    color_continuous_scale="RdBu_r",
    zmin=-1, zmax=1,
    text_auto=".2f",
    aspect="auto",
)
fig10.update_layout(margin=dict(t=10, b=10), height=550)
st.plotly_chart(fig10, use_container_width=True)
