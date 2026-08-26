"""EDOM Dashboard - Streamlit app for lecturer evaluation report visualization."""

import io

import streamlit as st

from src.chart_kriteria import generate_kriteria_chart
from src.chart_radar import generate_radar_chart
from src.chart_responden import generate_responden_chart
from src.data_loader import (
    filter_by_dosen,
    get_dosen_list,
    get_kriteria_list,
    load_and_prepare_data,
)
from src.utils import DATA_PATH, safe_filename


st.set_page_config(
    page_title="EDOM Dashboard",
    layout="wide",
)

st.title("Dashboard Rekap EDOM (Evaluasi Dosen oleh Mahasiswa)")


@st.cache_data(show_spinner=False)
def load_data():
    """Load and cache EDOM source data."""
    return load_and_prepare_data(DATA_PATH)


def fig_to_bytes(fig) -> bytes:
    """Convert a Plotly figure to PNG bytes only when requested."""
    buffer = io.BytesIO()
    fig.write_image(
        buffer,
        format="png",
        width=1400,
        height=900,
        scale=1,
    )
    return buffer.getvalue()


def get_cached_figure(cache_key: str, builder):
    """Return a figure from session memory or build it once."""
    if cache_key not in st.session_state:
        st.session_state[cache_key] = builder()

    return st.session_state[cache_key]


def show_png_download(fig, cache_key: str, filename: str):
    """Prepare a PNG only after request, then show one-click download."""
    png_key = f"{cache_key}_png"

    if png_key not in st.session_state:
        if st.button(
            "Siapkan Download PNG",
            key=f"{cache_key}_prepare",
        ):
            with st.spinner("Menyiapkan file PNG..."):
                st.session_state[png_key] = fig_to_bytes(fig)

    if png_key in st.session_state:
        st.download_button(
            label="⬇ Download PNG",
            data=st.session_state[png_key],
            file_name=filename,
            mime="image/png",
            key=f"{cache_key}_download",
            on_click="ignore",
        )


if not DATA_PATH.exists():
    st.error(f"File data tidak ditemukan: {DATA_PATH}")
    st.stop()

df = load_data()
dosen_list = get_dosen_list(df)
kriteria_list = get_kriteria_list(df)

if not dosen_list:
    st.warning("Data dosen belum tersedia.")
    st.stop()

st.sidebar.header("Filter")

selected_dosen = st.sidebar.selectbox(
    "Pilih Dosen",
    ["-- Pilih Dosen --"] + dosen_list,
)

st.sidebar.markdown(f"**Total Dosen:** {len(dosen_list)}")
st.sidebar.markdown(f"**Total Responden:** {len(df)}")

if selected_dosen == "-- Pilih Dosen --":
    st.info("Silakan pilih dosen dari sidebar untuk menampilkan data.")
    st.stop()

nama_dosen = selected_dosen
safe_dosen = safe_filename(nama_dosen)

df_dosen = filter_by_dosen(df, nama_dosen)

periode_counts = df_dosen["Periode"].value_counts().reindex(
    ["Pra UTS", "Pra UAS"],
    fill_value=0,
)

st.subheader(nama_dosen)
st.caption(f"Jumlah responden: {len(df_dosen)}")

col_uts, col_uas = st.columns(2)
col_uts.metric("Responden Pra UTS", int(periode_counts["Pra UTS"]))
col_uas.metric("Responden Pra UAS", int(periode_counts["Pra UAS"]))

# -------------------------------------------------------------------
# Line chart
# -------------------------------------------------------------------
with st.expander("Line Chart - Jumlah Responden", expanded=False):
    responden_cache_key = f"fig_responden_{safe_dosen}"

    fig_responden = get_cached_figure(
        responden_cache_key,
        lambda: generate_responden_chart(df_dosen, nama_dosen),
    )

    st.plotly_chart(
        fig_responden,
        use_container_width=True,
        key=f"plot_responden_{safe_dosen}",
    )

    show_png_download(
        fig_responden,
        responden_cache_key,
        f"line_responden_{safe_dosen}.png",
    )

# -------------------------------------------------------------------
# Radar charts
# -------------------------------------------------------------------
with st.expander("Radar Chart - Rata-rata Skor per Periode"):
    col_uts_radar, col_uas_radar = st.columns(2)

    for col, periode in zip(
        [col_uts_radar, col_uas_radar],
        ["Pra UTS", "Pra UAS"],
    ):
        with col:
            if periode_counts[periode] == 0:
                st.warning(f"Tidak ada data {periode} untuk dosen ini.")
                continue

            safe_periode = periode.replace(" ", "_")
            radar_cache_key = f"fig_radar_{safe_dosen}_{safe_periode}"

            fig_radar = get_cached_figure(
                radar_cache_key,
                lambda periode=periode: generate_radar_chart(
                    df_dosen,
                    kriteria_list,
                    periode,
                    nama_dosen,
                ),
            )

            st.plotly_chart(
                fig_radar,
                use_container_width=True,
                key=f"plot_radar_{safe_dosen}_{safe_periode}",
            )

            show_png_download(
                fig_radar,
                radar_cache_key,
                f"radar_{safe_periode}_{safe_dosen}.png",
            )

# -------------------------------------------------------------------
# Bar chart: one kriteria at a time, figure stored in Session State.
# -------------------------------------------------------------------
with st.expander("Bar Chart - Skor per Kriteria"):
    nav_key = f"kriteria_index_{safe_dosen}"

    if nav_key not in st.session_state:
        st.session_state[nav_key] = 0

    total_kriteria = len(kriteria_list)

    nav_prev, nav_info, nav_next = st.columns([1, 3, 1])

    with nav_prev:
        if st.button("⬅ Prev", key=f"prev_{safe_dosen}"):
            st.session_state[nav_key] = (
                st.session_state[nav_key] - 1
            ) % total_kriteria

    with nav_info:
        nomor_kriteria = st.session_state[nav_key] + 1
        st.markdown(
            (
                "<p style='text-align:center; font-weight:600; "
                "padding-top:8px;'>"
                f"Kriteria {nomor_kriteria} / {total_kriteria}"
                "</p>"
            ),
            unsafe_allow_html=True,
        )

    with nav_next:
        if st.button("Next ➡", key=f"next_{safe_dosen}"):
            st.session_state[nav_key] = (
                st.session_state[nav_key] + 1
            ) % total_kriteria

    current_index = st.session_state[nav_key]
    current_kriteria = kriteria_list[current_index]
    current_kriteria_safe = safe_filename(current_kriteria)

    bar_cache_key = (
        f"fig_bar_{safe_dosen}_{current_index}_{current_kriteria_safe}"
    )

    fig_bar = get_cached_figure(
        bar_cache_key,
        lambda: generate_kriteria_chart(
            df_dosen,
            current_kriteria,
            nama_dosen,
        ),
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True,
        key=f"plot_bar_{safe_dosen}_{current_index}",
    )

    show_png_download(
        fig_bar,
        bar_cache_key,
        f"kriteria_{current_index + 1:02d}_{safe_dosen}.png",
    )