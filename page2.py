"""
Page 2: Data Explorer — Tabel Interaktif dengan Filter
"""

import streamlit as st
import pandas as pd

# ── Load data ──────────────────────────────────────────────────
FILE_PATH = "bigdata_kelompok.csv"

@st.cache_data
def load_data():
    return pd.read_csv(FILE_PATH)

df = load_data()

st.title("🔍 Data Explorer")
st.markdown("Jelajahi data distribusi MBG secara interaktif. Gunakan filter di sidebar untuk menyaring data.")

# ── Sidebar Filters ────────────────────────────────────────────
st.sidebar.markdown("### 🎛️ Filter Data")

# Province filter
all_provinces = sorted(df["province"].unique())
selected_provinces = st.sidebar.multiselect(
    "Provinsi",
    options=all_provinces,
    default=[],
    placeholder="Semua provinsi",
)

# Beneficiary category filter
all_beneficiaries = sorted(df["beneficiary_category"].unique())
selected_beneficiaries = st.sidebar.multiselect(
    "Kategori Penerima",
    options=all_beneficiaries,
    default=[],
    placeholder="Semua kategori",
)

# Compliance tier filter
all_tiers = sorted(df["bgn_program_compliance_tier"].unique())
selected_tiers = st.sidebar.multiselect(
    "Tier Kepatuhan",
    options=all_tiers,
    default=[],
    placeholder="Semua tier",
)

# Protein type filter
all_proteins = sorted(df["protein_type"].unique())
selected_proteins = st.sidebar.multiselect(
    "Jenis Protein",
    options=all_proteins,
    default=[],
    placeholder="Semua jenis",
)

# Regional cluster filter
all_clusters = sorted(df["regional_cluster"].unique())
selected_clusters = st.sidebar.multiselect(
    "Klaster Wilayah",
    options=all_clusters,
    default=[],
    placeholder="Semua klaster",
)

# ── Apply Filters ──────────────────────────────────────────────
filtered = df.copy()

if selected_provinces:
    filtered = filtered[filtered["province"].isin(selected_provinces)]
if selected_beneficiaries:
    filtered = filtered[filtered["beneficiary_category"].isin(selected_beneficiaries)]
if selected_tiers:
    filtered = filtered[filtered["bgn_program_compliance_tier"].isin(selected_tiers)]
if selected_proteins:
    filtered = filtered[filtered["protein_type"].isin(selected_proteins)]
if selected_clusters:
    filtered = filtered[filtered["regional_cluster"].isin(selected_clusters)]

# ── Summary of filter ─────────────────────────────────────────
st.markdown(f"**Menampilkan {len(filtered):,} dari {len(df):,} data** "
            f"({len(filtered)/len(df)*100:.1f}%)")

# ── Quick Stats for Filtered Data ──────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Jumlah Data", f"{len(filtered):,}")
with col2:
    st.metric("Provinsi", f"{filtered['province'].nunique()}")
with col3:
    st.metric("Avg Biaya/Porsi", f"Rp{filtered['total_meal_cost_idr'].mean():,.0f}")
with col4:
    st.metric("Avg Kalori", f"{filtered['estimated_calories_kcal'].mean():,.0f} kkal")
with col5:
    st.metric("Avg Sisa Makanan", f"{filtered['plate_waste_percentage'].mean():.1f}%")

st.markdown("---")

# ── Column Selection ───────────────────────────────────────────
st.subheader("📋 Tabel Data")

# Columns to display (exclude the very long rationale column by default)
display_cols_default = [
    "distribution_id", "province", "regional_cluster", "beneficiary_category",
    "protein_type", "total_meal_cost_idr", "estimated_calories_kcal",
    "estimated_protein_grams", "plate_waste_percentage",
    "student_attendance_rate_pct", "local_farmer_sourcing_pct",
    "bgn_program_compliance_tier", "primary_food_waste_driver",
]

available_cols = list(filtered.columns)
selected_cols = st.multiselect(
    "Pilih kolom yang ditampilkan:",
    options=available_cols,
    default=display_cols_default,
)

if selected_cols:
    st.dataframe(
        filtered[selected_cols],
        use_container_width=True,
        height=500,
    )
else:
    st.warning("Pilih minimal satu kolom untuk ditampilkan.")

st.markdown("---")

# ── Descriptive Statistics ─────────────────────────────────────
st.subheader("📊 Statistik Deskriptif")

numeric_cols = filtered.select_dtypes(include="number").columns.tolist()
# Remove 'confidence_score' as it's not very informative
if "confidence_score" in numeric_cols:
    numeric_cols.remove("confidence_score")

st.dataframe(
    filtered[numeric_cols].describe().round(2).T,
    use_container_width=True,
)

st.markdown("---")

# ── Download ───────────────────────────────────────────────────
st.subheader("⬇️ Unduh Data")
st.markdown("Unduh data yang sudah difilter dalam format CSV.")

csv_data = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download CSV",
    data=csv_data,
    file_name="mbg_filtered_data.csv",
    mime="text/csv",
)
